# Extend Reservation Proxy with Payment Link

## Summary
Extend the `ReservationCreateProxyView` to support generating payment links (Stripe/PayPal) immediately after reservation creation, as per the external integration documentation.

## Problem
Currently, `ReservationCreateProxyView` only forwards the creation request to the legacy API and returns the reservation details. The frontend requires a payment link for non-cash reservations (Stripe/PayPal) to redirect the user for payment.

## Proposed Solution
1.  **Update `legacy_middleware/services.py`**:
    -   Add `_legacy_req` internal function to support both `GET` and `POST` methods (refactor `_post_to_legacy` for reuse).
    -   Add `fetch_payment_link` function to call `GET /api/v1/reservation/payment/handler`.
2.  **Update `legacy_middleware/views.py`**:
    -   Modify `ReservationCreateProxyView.post` method.
    -   After a successful reservation creation:
        -   Check if a payment method (`payment_method` parameter: `STRIPE` or `PAYPAL`) is provided.
        -   If explicitly `STRIPE` or `PAYPAL`:
            1.  Extract the `reservation_id` from the creation response (`config.id` or `id`).
            2.  Call `fetch_payment_link` using the auth token.
            3.  Return a JSON response containing ONLY the `payment_link`.
        -   If `payment_method` is CASH or missing/other:
            -   Proceed as before (return reservation details).

## Implementation Details

### `legacy_middleware/services.py`
Refactor `_post_to_legacy` -> `_request_to_legacy(method, endpoint, payload=None, params=None, ...)`.
*   Ensure `requests.request` or specific `requests.get`/`requests.post` calls are consistent.
*   Update `fetch_payment_link(token, reservation_id, type, language, success_url, cancel_url)` to use `GET` with query parameters.

### `legacy_middleware/views.py`
Algorithm for `ReservationCreateProxyView.post`:
1.  Get auth token (handled by `BaseLegacyProxyView` or manually if needed for both calls).
2.  Call `fetch_reservation_create`.
3.  On success (200 OK):
    -   `payment_method = request.data.get("payment_method")`
    -   If `payment_method` in `["STRIPE", "PAYPAL"]`:
        -   `reservation_id = extract_id(response.data)`
        -   Try `token = self.get_legacy_token().token`.
        -   `payment_url = services.fetch_payment_link(...)`
        -   Return `{"payment_link": payment_url}`
    -   Else:
        -   Return original response.

### `legacy_middleware/tests/`
**New Tests Required:**
1.  `test_services.py`:
    *   Test `fetch_payment_link` calls correct endpoint with correct query params (`type`, `id`, `language`, `success_url`, `cancel_url`).
    *   Verify headers construction for GET requests.
2.  `test_views.py` (`ReservationCreateProxyViewTestCase`):
    *   `test_create_success_stripe`: Input `payment_method="STRIPE"`. Mock reservation success -> Mock payment link success -> Verify response is valid JSON with `payment_link`.
    *   `test_create_success_paypal`: Input `payment_method="PAYPAL"`. Same flow.
    *   `test_create_payment_link_failure`: Reservation success -> Payment link 500/404 -> Verify 502 Bad Gateway response.
    *   `test_create_cash_ignored`: Input `payment_method="CASH"` or missing. Verify original reservation response is returned required.

**Refactoring Safety:**
*   Existing tests in `test_services.py` that mock `requests.post` must be updated if the implementation changes to `requests.request` or `requests.get`.


## Dependencies
- `requests`
