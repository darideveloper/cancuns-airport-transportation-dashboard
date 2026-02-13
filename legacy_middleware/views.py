from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import requests

from .services import fetch_legacy_autocomplete
from .models import LegacyAPIToken
from .services import fetch_legacy_token, fetch_quote


class AutocompleteProxyView(APIView):
    """
    Proxy view for the legacy autocomplete API.
    """

    permission_classes = [AllowAny]  # Since it's public for the frontend

    def post(self, request, *args, **kwargs):
        keyword = request.data.get("keyword")
        if not keyword:
            return Response(
                {"error": "Keyword is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            legacy_response = fetch_legacy_autocomplete(keyword)
            legacy_response.raise_for_status()
            return Response(legacy_response.json(), status=status.HTTP_200_OK)
        except requests.HTTPError as e:
            # Handle HTTP errors from legacy API
            if e.response.status_code == 422:
                return Response(
                    e.response.json(), status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            elif 400 <= e.response.status_code < 500:
                # Pass through client errors roughly? Or generic 400?
                # Design says "providing necessary feedback if it's a validation error".
                try:
                    return Response(e.response.json(), status=e.response.status_code)
                except:
                    return Response(
                        {"error": "Upstream client error"},
                        status=e.response.status_code,
                    )
            else:
                # 5xx errors from upstream -> 502 Bad Gateway
                return Response(
                    {"error": "Upstream service unavailable"},
                    status=status.HTTP_502_BAD_GATEWAY,
                )
        except requests.RequestException:
            # Network errors -> 502 Bad Gateway
            return Response(
                {"error": "Upstream service unreachable"},
                status=status.HTTP_502_BAD_GATEWAY,
            )


class QuoteProxyView(APIView):
    """
    Proxy view for the legacy Quote/Search API.
    Handles token authentication internally.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # 1. Get valid token
        token_obj = LegacyAPIToken.get_valid_token()

        if not token_obj:
            try:
                token, expires_at = fetch_legacy_token()
                token_obj = LegacyAPIToken.get_solo()
                token_obj.token = token
                token_obj.expires_at = expires_at
                token_obj.save()
            except requests.RequestException:
                return Response(
                    {"error": "Upstream authentication failed"},
                    status=status.HTTP_502_BAD_GATEWAY,
                )

        # 2. Call quote endpoint
        try:
            legacy_response = fetch_quote(token_obj.token, request.data)

            # Handle possible 401 if token expired unexpectedly or was revoked
            if legacy_response.status_code == 401:
                # Retry once with new token
                try:
                    token, expires_at = fetch_legacy_token()
                    token_obj = LegacyAPIToken.get_solo()
                    token_obj.token = token
                    token_obj.expires_at = expires_at
                    token_obj.save()
                    legacy_response = fetch_quote(token_obj.token, request.data)
                except requests.RequestException:
                    return Response(
                        {"error": "Upstream authentication failed during retry"},
                        status=status.HTTP_502_BAD_GATEWAY,
                    )

            # Pass through the response
            try:
                data = legacy_response.json()
            except ValueError:
                return Response(
                    {"error": "Invalid JSON from upstream"},
                    status=status.HTTP_502_BAD_GATEWAY,
                )

            # Validation Logic
            if legacy_response.status_code == 200:
                # 1. Pass through if upstream reports an application-level error (e.g. no_availability)
                if "error" in data:
                    return Response(data, status=status.HTTP_200_OK)

                # 2. Validate essential structure for success response
                has_items = isinstance(data.get("items"), list)
                has_places = isinstance(data.get("places"), dict)

                if not (has_items and has_places):
                    return Response(
                        {
                            "error": "Upstream response malformed: missing items or places"
                        },
                        status=status.HTTP_502_BAD_GATEWAY,
                    )

            return Response(data, status=legacy_response.status_code)

        except requests.RequestException:
            return Response(
                {"error": "Upstream service unreachable"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
