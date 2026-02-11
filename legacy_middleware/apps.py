from django.apps import AppConfig


class LegacyMiddlewareConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'legacy_middleware'
