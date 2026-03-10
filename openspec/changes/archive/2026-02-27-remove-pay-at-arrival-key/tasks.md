# Tasks: Remove 'pay_at_arrival' key from Reservation API

## Summary
A step-by-step guide to removing the `pay_at_arrival` key from the entire reservation process.

## Tasks

### 1. Preparation & Exploration
- [x] Confirm no other system (outside the middleware) depends on `pay_at_arrival` in the local DB.

### 2. Code Modification: Middleware
- [x] Update `legacy_middleware.views.ReservationCreateProxyView` to strip `pay_at_arrival` from the request data before proxying.
- [x] Refactor the view to use the cleaned data consistently.

### 3. Test Updates
- [x] Update `legacy_middleware/tests/test_views.py` to remove `pay_at_arrival` from all `reservation_payload` objects.
- [x] Ensure that "cash" tests (those without `STRIPE` or `PAYPAL`) still pass without `pay_at_arrival`.
- [x] Run all middleware tests: `python manage.py test legacy_middleware`.

### 4. Documentation & Specification Cleanup
- [x] Modify `openspec/specs/reservation-proxy/spec.md` to remove any references to `pay_at_arrival`.
- [x] Sanitize all `docs/*.md` files, removing `pay_at_arrival` from tables, JSON examples, and text descriptions.
- [x] Remove `pay_at_arrival` from the newly created `docs/sale-api.md`.

### 5. Final Verification
- [x] Perform a global search for `pay_at_arrival` to ensure no traces remain in `.py` or `.md` files.
- [x] Verify that Stripe/PayPal flows are unaffected by the removal.
