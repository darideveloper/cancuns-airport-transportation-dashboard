from django.urls import path
from .views import AutocompleteProxyView, QuoteProxyView

urlpatterns = [
    path(
        "legacy/autocomplete/",
        AutocompleteProxyView.as_view(),
        name="legacy_autocomplete",
    ),
    path("legacy/quote/", QuoteProxyView.as_view(), name="legacy_quote"),
]
