# Tasks: Integrate Multi-Payment Checkout

## Initial Setup
- [x] Initialize proposal and design documents. <!-- id: 0 -->

## Middleware Services
- [x] Add `fetch_payment_capture_order` to `legacy_middleware/services.py`. <!-- id: 1 -->
- [x] Add `PaymentCaptureProxyView` to `legacy_middleware/views.py`. <!-- id: 2 -->
- [x] Register `legacy/capture/` route in `legacy_middleware/urls.py`. <!-- id: 3 -->

## Middleware Logic Updates
- [x] Update `ReservationCreateProxyView.post` in `legacy_middleware/views.py` to map `CREDIT_CARD` to `PAYPAL`. <!-- id: 4 -->
- [x] Update success response in `ReservationCreateProxyView.post` to include `paypal_id`, `uuid`, and `reservation_id`. <!-- id: 5 -->

## Verification & Testing
- [x] Update `ReservationCreateProxyViewTestCase` in `legacy_middleware/tests/test_views.py` with the new response structure. <!-- id: 6 -->
- [x] Add `test_create_success_credit_card_mapping` to `legacy_middleware/tests/test_views.py`. <!-- id: 7 -->
- [x] Add `PaymentCaptureProxyViewTestCase` to `legacy_middleware/tests/test_views.py`. <!-- id: 8 -->
- [x] Run all middleware tests: `python manage.py test legacy_middleware`. <!-- id: 9 -->

## Documentation
- [x] Update `docs/checkout-paypal-analysis.md` with the finalized flow and code changes. <!-- id: 10 -->
