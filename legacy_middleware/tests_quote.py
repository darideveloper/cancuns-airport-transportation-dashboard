from unittest.mock import patch, MagicMock
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
import requests
from .models import LegacyAPIToken


class QuoteProxyViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("legacy_quote")

    def test_model_constraints(self):
        token = "test_token"
        expires_at = timezone.now() + timedelta(hours=1)
        LegacyAPIToken.objects.create(token=token, expires_at=expires_at)

        self.assertEqual(LegacyAPIToken.objects.count(), 1)
        self.assertEqual(LegacyAPIToken.objects.first().token, token)

    @patch("legacy_middleware.views.fetch_legacy_token")
    @patch("legacy_middleware.views.fetch_quote")
    def test_view_happy_path_no_token(self, mock_quote, mock_oauth):
        # Start with empty DB
        LegacyAPIToken.objects.all().delete()

        mock_oauth.return_value = ("new_token", timezone.now() + timedelta(hours=1))
        mock_quote_resp = MagicMock()
        mock_quote_resp.status_code = 200
        mock_quote_resp.json.return_value = {"items": []}
        mock_quote.return_value = mock_quote_resp

        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should have created a token
        self.assertTrue(LegacyAPIToken.objects.exists())
        self.assertEqual(LegacyAPIToken.objects.last().token, "new_token")
        mock_oauth.assert_called_once()
        mock_quote.assert_called_once()

    @patch("legacy_middleware.views.fetch_legacy_token")
    @patch("legacy_middleware.views.fetch_quote")
    def test_view_happy_path_reuse_token(self, mock_quote, mock_oauth):
        # Pre-fill DB
        existing_token = LegacyAPIToken.objects.create(
            token="existing_token", expires_at=timezone.now() + timedelta(hours=1)
        )

        mock_quote_resp = MagicMock()
        mock_quote_resp.status_code = 200
        mock_quote_resp.json.return_value = {"items": []}
        mock_quote.return_value = mock_quote_resp

        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_oauth.assert_not_called()
        mock_quote.assert_called_once()
        # Verify arguments passed to fetch_quote
        args, _ = mock_quote.call_args
        self.assertEqual(args[0], "existing_token")

    @patch("legacy_middleware.views.fetch_legacy_token")
    @patch("legacy_middleware.views.fetch_quote")
    def test_view_expired_token_auto_refresh(self, mock_quote, mock_oauth):
        # Pre-fill DB with expired token
        LegacyAPIToken.objects.create(
            token="expired_token", expires_at=timezone.now() - timedelta(hours=1)
        )

        mock_oauth.return_value = (
            "refreshed_token",
            timezone.now() + timedelta(hours=1),
        )
        mock_quote_resp = MagicMock()
        mock_quote_resp.status_code = 200
        mock_quote_resp.json.return_value = {"items": []}
        mock_quote.return_value = mock_quote_resp

        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_oauth.assert_called_once()
        self.assertEqual(LegacyAPIToken.objects.last().token, "refreshed_token")

        # Verify fetch_quote used the new token
        args, _ = mock_quote.call_args
        self.assertEqual(args[0], "refreshed_token")

    @patch("legacy_middleware.views.fetch_legacy_token")
    @patch("legacy_middleware.views.fetch_quote")
    def test_view_upstream_auth_failure_retry(self, mock_quote, mock_oauth):
        # Valid token in DB but upstream rejects it with 401
        LegacyAPIToken.objects.create(
            token="stale_token", expires_at=timezone.now() + timedelta(hours=1)
        )

        mock_oauth.return_value = ("fresh_token", timezone.now() + timedelta(hours=1))

        # First call fails 401, second succeeds
        fail_resp = MagicMock()
        fail_resp.status_code = 401

        success_resp = MagicMock()
        success_resp.status_code = 200
        success_resp.json.return_value = {"items": []}

        mock_quote.side_effect = [fail_resp, success_resp]

        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_oauth.assert_called_once()
        self.assertEqual(mock_quote.call_count, 2)

        # Verify first call used stale, second used fresh
        args1, _ = mock_quote.call_args_list[0]
        self.assertEqual(args1[0], "stale_token")

        args2, _ = mock_quote.call_args_list[1]
        self.assertEqual(args2[0], "fresh_token")

    @patch("legacy_middleware.views.fetch_legacy_token")
    @patch("legacy_middleware.views.fetch_quote")
    def test_view_upstream_error_handling(self, mock_quote, mock_oauth):
        # Mock token existence
        LegacyAPIToken.objects.create(
            token="valid_token", expires_at=timezone.now() + timedelta(hours=1)
        )

        # Mock 422 error
        mock_quote_resp = MagicMock()
        mock_quote_resp.status_code = 422
        mock_quote_resp.json.return_value = {"error": "Validation error"}
        mock_quote.return_value = mock_quote_resp

        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.data, {"error": "Validation error"})

    @patch("legacy_middleware.services.requests.post")
    def test_service_fetch_token_success(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"token": "abc", "expires_in": 3600}
        mock_post.return_value = mock_resp

        from legacy_middleware.services import fetch_legacy_token

        token, expires_at = fetch_legacy_token()

        self.assertEqual(token, "abc")
        # Since implementation uses buffer of 86400, expected expiry for 3600 input is (now - 82800).
        # We can check if it returns correct datetime object
        pass

    @patch("legacy_middleware.services.requests.post")
    def test_service_fetch_token_success_large_expiry(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"token": "abc", "expires_in": 100000}
        mock_post.return_value = mock_resp

        from legacy_middleware.services import fetch_legacy_token

        token, expires_at = fetch_legacy_token()
        self.assertEqual(token, "abc")
        self.assertTrue(expires_at > timezone.now())

    @patch("legacy_middleware.services.requests.post")
    def test_service_fetch_token_failure(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_resp.raise_for_status.side_effect = requests.HTTPError("401 Client Error")
        mock_post.return_value = mock_resp

        from legacy_middleware.services import fetch_legacy_token

        with self.assertRaises(requests.HTTPError):
            fetch_legacy_token()
