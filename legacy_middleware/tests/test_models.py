from django.test import TestCase
from legacy_middleware.models import LegacyAPIToken
from django.utils import timezone
from datetime import timedelta


class LegacyAPITokenModelTest(TestCase):
    def test_singleton_behavior(self):
        """Test that only one instance of LegacyAPIToken can exist."""
        token1 = LegacyAPIToken.get_solo()
        token1.token = "token1"
        token1.expires_at = timezone.now() + timedelta(hours=1)
        token1.save()

        token2 = LegacyAPIToken.get_solo()
        token2.token = "token2"
        token2.save()

        # Should still be only one row in DB
        self.assertEqual(LegacyAPIToken.objects.count(), 1)

        # The instance should have the last saved data
        instance = LegacyAPIToken.get_solo()
        self.assertEqual(instance.token, "token2")

    def test_get_valid_token_expired(self):
        """Test get_valid_token returns None if expired."""
        instance = LegacyAPIToken.get_solo()
        instance.token = "expired_token"
        instance.expires_at = timezone.now() - timedelta(hours=1)
        instance.save()

        self.assertIsNone(LegacyAPIToken.get_valid_token())

    def test_get_valid_token_valid(self):
        """Test get_valid_token returns the instance if valid."""
        instance = LegacyAPIToken.get_solo()
        instance.token = "valid_token"
        instance.expires_at = timezone.now() + timedelta(hours=1)
        instance.save()

        valid_token_obj = LegacyAPIToken.get_valid_token()
        self.assertIsNotNone(valid_token_obj)
        self.assertEqual(valid_token_obj.token, "valid_token")
