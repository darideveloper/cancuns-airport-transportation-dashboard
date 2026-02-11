from unittest.mock import patch
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import requests


class AutocompleteProxyViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("legacy_autocomplete")

    @override_settings(
        LEGACY_API_KEY="test-api-key", LEGACY_API_BASE_URL="http://test-api.com"
    )
    @patch("legacy_middleware.services.requests.post")
    def test_autocomplete_success(self, mock_post):
        """
        Verify the Django view returns 200 OK with the mocked list of locations.
        """
        # Mock successful response from legacy API
        mock_response = requests.Response()
        mock_response.status_code = 200
        expected_data = {"items": [{"id": 1, "name": "Cancun Airport"}]}
        mock_response._content = b'{"items": [{"id": 1, "name": "Cancun Airport"}]}'
        mock_response.json = lambda: expected_data
        mock_post.return_value = mock_response

        # Request to Django view
        response = self.client.post(self.url, {"keyword": "cancun"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)

        # Verify call to legacy API (Task 7 implicit coverage)
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs["headers"]["app-key"], "test-api-key")
        self.assertIn("http://test-api.com", args[0])
        self.assertEqual(kwargs["json"]["keyword"], "cancun")

    def test_autocomplete_validation(self):
        """
        Verify 400 Bad Request when keyword is missing.
        """
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Should verify service is NOT called, but we need to mock it to fail if called
        with patch("legacy_middleware.services.requests.post") as mock_post:
            response = self.client.post(self.url, {}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            mock_post.assert_not_called()

    @override_settings(
        LEGACY_API_KEY="test-api-key", LEGACY_API_BASE_URL="http://test-api.com"
    )
    @patch("legacy_middleware.services.requests.post")
    def test_autocomplete_external_error(self, mock_post):
        """
        Verify graceful error handling (502) when legacy API fails.
        """
        # Mock connection error
        mock_post.side_effect = requests.RequestException("Connection error")

        response = self.client.post(self.url, {"keyword": "fail"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)

    @override_settings(
        LEGACY_API_KEY="test-api-key", LEGACY_API_BASE_URL="http://test-api.com"
    )
    @patch("legacy_middleware.services.requests.post")
    def test_autocomplete_legacy_500(self, mock_post):
        """
        Verify handling of 500 from legacy API.
        """
        mock_response = requests.Response()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        response = self.client.post(self.url, {"keyword": "error"}, format="json")
        # Depending on implementation, we might want to pass through the 500 or wrap it.
        # Design says: "wraps this in a generic error response (e.g., 502 Bad Gateway)"
        # So expecting 502 is reasonable if upstream is 500.
        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)
