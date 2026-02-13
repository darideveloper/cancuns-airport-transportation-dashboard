from django.db import models
from django.utils import timezone
from solo.models import SingletonModel


# Create your models here.
class LegacyAPIToken(SingletonModel):
    token = models.TextField()
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_valid_token(cls):
        """Fetch a valid token from the database."""
        instance = cls.get_solo()
        if not instance.token or not instance.expires_at:
            return None
        if instance.expires_at <= timezone.now():
            return None
        return instance
