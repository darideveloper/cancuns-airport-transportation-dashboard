from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import requests

from .services import fetch_legacy_autocomplete
from .models import LegacyAPIToken
from .services import fetch_legacy_token, fetch_quote, fetch_reservation_create


class BaseLegacyProxyView(APIView):
    """
    Common base for legacy proxy views handling auth, retry, and error mapping.
    """

    permission_classes = [AllowAny]

    def get_legacy_token(self):
        """Get a valid token from cache/DB or fetch a new one."""
        token_obj = LegacyAPIToken.get_valid_token()
        if not token_obj:
            token, expires_at = fetch_legacy_token()
            token_obj = LegacyAPIToken.get_solo()
            token_obj.token = token
            token_obj.expires_at = expires_at
            token_obj.save()
        return token_obj

    def execute_proxy_request(
        self, request_func, payload, requires_auth=True, validate_func=None
    ):
        """Standard flow for all proxy requests."""
        try:
            token = None
            if requires_auth:
                try:
                    token_obj = self.get_legacy_token()
                    token = token_obj.token
                except requests.RequestException:
                    return Response(
                        {"error": "Upstream authentication failed"},
                        status=status.HTTP_502_BAD_GATEWAY,
                    )

            response = (
                request_func(token, payload) if requires_auth else request_func(payload)
            )

            # Retry on 401
            if requires_auth and response.status_code == 401:
                try:
                    token, expires_at = fetch_legacy_token()
                    token_obj = LegacyAPIToken.get_solo()
                    token_obj.token = token
                    token_obj.expires_at = expires_at
                    token_obj.save()
                    response = request_func(token, payload)
                except requests.RequestException:
                    return Response(
                        {"error": "Upstream authentication failed during retry"},
                        status=status.HTTP_502_BAD_GATEWAY,
                    )

            # JSON Parsing
            try:
                data = response.json()
            except ValueError:
                return Response(
                    {"error": "Invalid JSON from upstream"},
                    status=status.HTTP_502_BAD_GATEWAY,
                )

            # Optional application-level validation
            if response.status_code == 200 and validate_func:
                validation_error = validate_func(data)
                if validation_error:
                    return validation_error

            # Error mapping
            if response.status_code >= 400:
                if response.status_code == 422:
                    return Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                elif response.status_code >= 500:
                    return Response(
                        {"error": "Upstream service unavailable"},
                        status=status.HTTP_502_BAD_GATEWAY,
                    )
                return Response(data, status=response.status_code)

            return Response(data, status=response.status_code)

        except requests.RequestException:
            return Response(
                {"error": "Upstream service unreachable"},
                status=status.HTTP_502_BAD_GATEWAY,
            )


class AutocompleteProxyView(BaseLegacyProxyView):
    """
    Proxy view for the legacy autocomplete API.
    """

    def post(self, request, *args, **kwargs):
        keyword = request.data.get("keyword")
        if not keyword:
            return Response(
                {"error": "Keyword is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        return self.execute_proxy_request(
            fetch_legacy_autocomplete, keyword, requires_auth=False
        )


class QuoteProxyView(BaseLegacyProxyView):
    """
    Proxy view for the legacy Quote/Search API.
    Handles token authentication internally.
    """

    def validate_quote_structure(self, data):
        # 1. Pass through if upstream reports an application-level error (e.g. no_availability)
        if "error" in data:
            return None  # Let it pass through as OK

        # 2. Validate essential structure for success response
        has_items = isinstance(data.get("items"), list)
        has_places = isinstance(data.get("places"), dict)

        if not (has_items and has_places):
            return Response(
                {"error": "Upstream response malformed: missing items or places"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        return None

    def post(self, request, *args, **kwargs):
        return self.execute_proxy_request(
            fetch_quote, request.data, validate_func=self.validate_quote_structure
        )


class ReservationCreateProxyView(BaseLegacyProxyView):
    """
    Proxy view for the legacy Reservation Create API.
    Handles token authentication internally.
    """

    def validate_reservation_response(self, data):
        """
        Validate the structure of a successful reservation creation response.

        Returns None if valid, or a Response object with error details if invalid.
        """
        # 0. Safety check: Ensure data is a dictionary
        if not isinstance(data, dict):
            return Response(
                {"error": "Upstream response malformed: expected JSON object"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        # 1. Pass through if upstream reports an application-level error
        if "error" in data:
            return None

        # 2. Check for success indicators
        # The legacy API typically returns 'reservation_id' or 'id' on success.
        has_id = "reservation_id" in data or "id" in data

        if not has_id:
            return Response(
                {"error": "Upstream response malformed: missing reservation ID"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        return None

    def post(self, request, *args, **kwargs):
        return self.execute_proxy_request(
            fetch_reservation_create,
            request.data,
            validate_func=self.validate_reservation_response,
        )
