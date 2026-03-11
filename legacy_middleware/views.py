from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import requests

from .services import fetch_legacy_autocomplete
from .models import LegacyAPIToken
from .services import (
    fetch_legacy_token,
    fetch_quote,
    fetch_reservation_create,
    fetch_payment_link,
    fetch_payment_capture_order,
    fetch_my_booking,
)


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
        # The legacy API typically returns 'reservation_id' or 'id' on success,
        # often nested inside a 'config' object.
        has_id = (
            "reservation_id" in data
            or "id" in data
            or (
                "config" in data
                and isinstance(data["config"], dict)
                and ("id" in data["config"] or "code" in data["config"])
            )
        )

        if not has_id:
            return Response(
                {"error": "Upstream response malformed: missing reservation ID"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        return None

    def extract_reservation_id(self, data):
        """Helper to safely extract the reservation ID from various response formats."""
        if isinstance(data, dict):
            if "reservation_id" in data:
                return data["reservation_id"]
            if "id" in data:
                return data["id"]
            if "config" in data and isinstance(data["config"], dict):
                if "id" in data["config"]:
                    return data["config"]["id"]
                if "code" in data["config"]:
                    return data["config"]["code"]
        return None

    def extract_uuid(self, data):
        """Helper to safely extract the UUID from various response formats."""
        if isinstance(data, dict):
            if "uuid" in data:
                return data["uuid"]
            if "config" in data and isinstance(data["config"], dict):
                if "uuid" in data["config"]:
                    return data["config"]["uuid"]
        return None

    def post(self, request, *args, **kwargs):
        # 1. Prepare Payload & Handle CASH
        original_payment_method = request.data.get("payment_method")
        payment_method_str = str(original_payment_method).upper() if original_payment_method else ""
        
        payload = request.data.copy()

        # Field Mapping for Legacy Compatibility
        mapping = {
            "flightNumber": "flight_number",
            "notes": "comments",
            "firstName": "first_name",
            "lastName": "last_name",
            "email": "email_address"
        }

        for front_key, back_key in mapping.items():
            if front_key in payload:
                payload[back_key] = payload.pop(front_key)

        if payment_method_str == "CASH":
            payload["pay_at_arrival"] = 1
        else:
            # Ensure it's not present if not CASH
            payload.pop("pay_at_arrival", None)

        # 2. Create Reservation
        response = self.execute_proxy_request(
            fetch_reservation_create,
            payload,
            validate_func=self.validate_reservation_response,
        )

        if response.status_code != 200:
            return response

        reservation_data = response.data
        if isinstance(reservation_data, dict) and "error" in reservation_data:
            return response

        reservation_id = self.extract_reservation_id(reservation_data)
        uuid = self.extract_uuid(reservation_data)

        # 3. Check for Payment Generation Requirement (Stripe/PayPal)
        # Map CREDIT_CARD to PAYPAL as we are using PayPal Cards now
        # Map to PAYPAL-V2 for modern SDK support
        payment_provider = payment_method_str
        if payment_provider == "CREDIT_CARD":
            payment_provider = "PAYPAL-V2"
        elif payment_provider == "PAYPAL":
            payment_provider = "PAYPAL-V2"

        if payment_provider in ["STRIPE", "PAYPAL-V2"]:
            # Fallback if extract helper failed but validation passed (should be rare)
            if not reservation_id:
                return Response(
                    {
                        "error": "Failed to extract reservation ID for payment link generation"
                    },
                    status=status.HTTP_502_BAD_GATEWAY,
                )

            # 4. Get Payment Link
            try:
                # Reuse token from cache handling in base view
                token_obj = self.get_legacy_token()

                cancel_val = request.data.get("cancel_url")
                success_val = request.data.get("success_url")

                # Fetch payment link (Pass absolute URLs directly)
                payment_response = fetch_payment_link(
                    token=token_obj.token,
                    reservation_id=reservation_id,
                    payment_provider=payment_provider,
                    language=request.data.get("language", "en"),
                    success_url=success_val,
                    cancel_url=cancel_val,
                )

                # Custom handling for non-200 payment responses
                if payment_response.status_code != 200:
                    try:
                        error_detail = payment_response.json()
                    except ValueError:
                        error_detail = "Unknown upstream error"
                    
                    return Response(
                        {
                            "error": "Failed to initialize payment with upstream provider",
                            "upstream_error": error_detail,
                            "reservation_id": reservation_id,
                            "uuid": uuid
                        },
                        status=status.HTTP_502_BAD_GATEWAY,
                    )

                # Parse JSON
                try:
                    link_data = payment_response.json()
                except ValueError:
                    return Response(
                        {"error": "Invalid JSON from payment provider upstream"},
                        status=status.HTTP_502_BAD_GATEWAY,
                    )

                # 5. Return standardized response
                response_payload = {
                    "reservation_id": reservation_id,
                    "uuid": uuid,
                    "payment_method": original_payment_method,
                    "payment_data": link_data
                }

                # Hoist paypal_id if present with safety check and provider-specific fallback
                if isinstance(link_data, dict):
                    if "paypal_id" in link_data:
                        response_payload["paypal_id"] = link_data["paypal_id"]
                    elif payment_provider == "PAYPAL-V2" and "url" in link_data:
                        # For PAYPAL-V2, 'url' field contains the actual Order ID
                        response_payload["paypal_id"] = link_data["url"]

                return Response(response_payload, status=status.HTTP_200_OK)

            except Exception as e:
                # Catch requests.RequestException or other errors
                return Response(
                    {
                        "error": "Failed to generate payment link",
                        "detail": str(e),
                        "reservation_id": reservation_id,
                        "uuid": uuid
                    },
                    status=status.HTTP_502_BAD_GATEWAY,
                )

        # Standardized response for CASH or other non-online methods
        return Response({
            "reservation_id": reservation_id,
            "uuid": uuid,
            "payment_method": original_payment_method,
            "payment_data": {}
        }, status=status.HTTP_200_OK)


class PaymentCaptureProxyView(BaseLegacyProxyView):
    """
    Proxy view for the legacy PayPal Capture API.
    GET /api/v1/reservation/payment/paypal/capture-order
    """

    def post(self, request, *args, **kwargs):
        order_id = request.data.get("id")
        if not order_id:
            return Response(
                {"error": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        return self.execute_proxy_request(fetch_payment_capture_order, order_id)


class MyBookingProxyView(BaseLegacyProxyView):
    """
    Proxy view for retrieving existing reservation details.
    """

    def validate_my_booking_response(self, data):
        """
        Validate the structure of a successful reservation retrieval response.
        """
        if not isinstance(data, dict):
            return Response(
                {"error": "Upstream response malformed: expected JSON object"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        # Legacy API might return 'error' as a key even with HTTP 200
        if "error" in data:
            return None

        # Check for essential fields defined in api-integration-my-booking.md
        # Status and client are usually present in a valid reservation object
        if "status" not in data and "items" not in data:
            return Response(
                {"error": "Upstream response malformed: missing reservation data"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return None

    def post(self, request, *args, **kwargs):
        # Validate required input
        code = request.data.get("code")
        email = request.data.get("email")

        if not code or not email:
            return Response(
                {"error": "Both 'code' and 'email' are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return self.execute_proxy_request(
            fetch_my_booking,
            request.data,
            validate_func=self.validate_my_booking_response,
        )
