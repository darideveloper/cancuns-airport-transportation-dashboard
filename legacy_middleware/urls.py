from django.urls import path
from .views import (
    AutocompleteProxyView,
    QuoteProxyView,
    ReservationCreateProxyView,
    MyBookingProxyView,
)

urlpatterns = [
    path(
        "legacy/autocomplete/",
        AutocompleteProxyView.as_view(),
        name="legacy_autocomplete",
    ),
    path("legacy/quote/", QuoteProxyView.as_view(), name="legacy_quote"),
    path(
        "legacy/create/",
        ReservationCreateProxyView.as_view(),
        name="legacy_reservation_create",
    ),
    path(
        "legacy/my-booking/",
        MyBookingProxyView.as_view(),
        name="legacy_my_booking",
    ),
]
