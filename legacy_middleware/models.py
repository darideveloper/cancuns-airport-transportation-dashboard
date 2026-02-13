from django.db import models
from django.utils import timezone


# Create your models here.
class LegacyAPIToken(models.Model):
    token = models.TextField()
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_valid_token(cls):
        """Fetch a valid token from the database."""
        return cls.objects.filter(expires_at__gt=timezone.now()).first()
