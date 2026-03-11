# Tasks: Fix Payment Integration Logic

## Setup & Research
- [x] Verify `type=PAYPAL-V2` in legacy docs (already done via analysis).

## Implementation

### 1. Legacy Service Update
- [x] Update `fetch_payment_link` in `legacy_middleware/services.py` to handle any string provider type correctly (it already does, but verify if mapping is needed in service layer).

### 2. View Logic Refactoring
- [x] Update `ReservationCreateProxyView.post` in `legacy_middleware/views.py`:
  - [x] Inject `"pay_at_arrival": 1` for `CASH` reservations.
  - [x] Use `PAYPAL-V2` instead of `PAYPAL` for the payment handler call.
  - [x] Standardize the final response JSON structure for all payment methods.
  - [x] Preserve the original `payment_method` in the response.
  - [x] Refine 502 error handling to provide more specific feedback when payment initialization fails.
  - [x] Verify URL handling to prevent domain duplication in success/cancel URLs.

### 3. Validation & Testing
- [x] Update `legacy_middleware/tests/test_views.py`:
  - [x] Add test case for `CASH` reservation verifying `pay_at_arrival` injection.
  - [x] Add test case for `PAYPAL` verifying `type=PAYPAL-V2` upstream call.
  - [x] Add test case for `CREDIT_CARD` verifying internal mapping but original method preservation.
- [x] Run `python manage.py test legacy_middleware.tests.test_views` and ensure all tests pass.
