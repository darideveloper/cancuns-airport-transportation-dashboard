
from django.urls import path
from .views import AutocompleteProxyView

urlpatterns = [
    path("legacy/autocomplete/", AutocompleteProxyView.as_view(), name="legacy_autocomplete"),
]
