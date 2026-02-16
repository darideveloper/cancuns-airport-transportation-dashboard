from unittest.mock import MagicMock, patch

from django.test import TestCase, override_settings

from legacy_middleware.services import (
    fetch_quote,
    fetch_reservation_create,
    fetch_payment_link,
    fetch_my_booking,
)


class FetchReservationCreateTests(TestCase):
    """
    Test the fetch_reservation_create service function directly.
    This verifies parameter injection logic that was previously untested.
    """

    @override_settings(
        LEGACY_API_BASE_URL="http://test-api.com",
        LEGACY_API_SITE_ID="123",
    )
    @patch("legacy_middleware.services.requests.post")
    def test_fetch_reservation_create_injects_site_id(self, mock_post):
        """
        Verify site_id is injected from settings when missing in payload.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"reservation_id": "ABC123"}
        mock_post.return_value = mock_response

        token = "test_token"
        payload = {"customer_name": "John Doe"}

        fetch_reservation_create(token, payload)

        # Verify the request was made
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args

        # Verify URL
        self.assertEqual(args[0], "http://test-api.com/api/v1/create")

        # Verify site_id was injected
        self.assertEqual(kwargs["json"]["site_id"], 123)
        self.assertEqual(kwargs["json"]["customer_name"], "John Doe")

        # Verify Authorization header
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer test_token")

    @override_settings(
        LEGACY_API_BASE_URL="http://test-api.com",
        LEGACY_API_SITE_ID="123",
    )
    @patch("legacy_middleware.services.requests.post")
    def test_fetch_reservation_create_preserves_site_id(self, mock_post):
        """
        Verify existing site_id in payload is not overwritten.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"reservation_id": "ABC123"}
        mock_post.return_value = mock_response

        token = "test_token"
        payload = {"customer_name": "John Doe", "site_id": 999}

        fetch_reservation_create(token, payload)

        # Verify the request was made
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args

        # Verify site_id was NOT overwritten
        self.assertEqual(kwargs["json"]["site_id"], 999)
        self.assertEqual(kwargs["json"]["customer_name"], "John Doe")

    @override_settings(
        LEGACY_API_BASE_URL="http://test-api.com",
        LEGACY_API_SITE_ID="456",
    )
    @patch("legacy_middleware.services.requests.post")
    def test_fetch_reservation_create_auth_header(self, mock_post):
        """
        Verify correct Authorization: Bearer <token> header is sent.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"reservation_id": "XYZ789"}
        mock_post.return_value = mock_response

        token = "my_secret_token"
        payload = {"customer_name": "Jane Smith"}

        fetch_reservation_create(token, payload)

        # Verify the request was made
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args

        # Verify Authorization header format
        self.assertIn("Authorization", kwargs["headers"])
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer my_secret_token")

        # Verify Content-Type header
        self.assertEqual(kwargs["headers"]["Content-Type"], "application/json")


class FetchQuoteTests(TestCase):
    """
    Test the fetch_quote service function directly.
    Bonus cleanup to verify rate_group injection.
    """

    @override_settings(
        LEGACY_API_BASE_URL="http://test-api.com",
        LEGACY_API_RATE_GROUP="premium",
    )
    @patch("legacy_middleware.services.requests.post")
    def test_fetch_quote_injects_rate_group(self, mock_post):
        """
        Verify rate_group is injected from settings when missing.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [], "places": {}}
        mock_post.return_value = mock_response

        token = "test_token"
        payload = {"origin": "A", "destination": "B"}

        fetch_quote(token, payload)

        # Verify the request was made
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args

        # Verify URL
        self.assertEqual(args[0], "http://test-api.com/api/v1/quote")

        # Verify rate_group was injected
        self.assertEqual(kwargs["json"]["rate_group"], "premium")
        self.assertEqual(kwargs["json"]["origin"], "A")
        self.assertEqual(kwargs["json"]["destination"], "B")

        # Verify Authorization header
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer test_token")

    @override_settings(
        LEGACY_API_BASE_URL="http://test-api.com",
        LEGACY_API_RATE_GROUP="premium",
    )
    @patch("legacy_middleware.services.requests.post")
    def test_fetch_quote_preserves_rate_group(self, mock_post):
        """
        Verify existing rate_group in payload is not overwritten.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [], "places": {}}
        mock_post.return_value = mock_response

        token = "test_token"
        payload = {"origin": "A", "destination": "B", "rate_group": "vip"}

        fetch_quote(token, payload)

        # Verify the request was made
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args

        # Verify rate_group was NOT overwritten
        self.assertEqual(kwargs["json"]["rate_group"], "vip")


class FetchPaymentLinkTests(TestCase):
    """
    Test the fetch_payment_link service function.
    """

    @override_settings(
        LEGACY_API_BASE_URL="http://test-api.com",
    )
    @patch("legacy_middleware.services.requests.get")
    def test_fetch_payment_link_calls_correct_endpoint(self, mock_get):
        """
        Verify correct URL, method, and parameters are passed.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"url": "http://stripe.com/pay"}
        mock_get.return_value = mock_response

        token = "test_token"
        reservation_id = 12345
        payment_provider = "STRIPE"
        language = "en"
        success_url = "http://success.com"
        cancel_url = "http://cancel.com"

        fetch_payment_link(
            token, reservation_id, payment_provider, language, success_url, cancel_url
        )

        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args

        # Verify URL
        self.assertEqual(
            args[0], "http://test-api.com/api/v1/reservation/payment/handler"
        )

        # Verify Headers
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer test_token")

        # Verify Params
        expected_params = {
            "type": "STRIPE",
            "id": 12345,
            "language": "en",
            "success_url": "http://success.com",
            "cancel_url": "http://cancel.com",
        }
        self.assertEqual(kwargs["params"], expected_params)


class FetchMyBookingServiceTests(TestCase):
    """
    Unit tests for the fetch_my_booking service function.
    """

    @override_settings(
        LEGACY_API_BASE_URL="http://test-api.com", LEGACY_API_SITE_ID="25"
    )
    @patch("legacy_middleware.services.requests.post")
    def test_fetch_my_booking_calls_correct_endpoint(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "CONFIRMED"}
        mock_post.return_value = mock_response

        token = "test_token"
        payload = {"code": "ABC123", "email": "test@example.com", "language": "en"}
        response = fetch_my_booking(token, payload)

        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "http://test-api.com/api/v1/reservation/get")
        self.assertEqual(kwargs["json"]["code"], "ABC123")
        self.assertEqual(kwargs["json"]["site_id"], 25)
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer test_token")
        self.assertEqual(response.status_code, 200)
