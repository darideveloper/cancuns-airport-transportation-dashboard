# Tasks: Fix After-Payment Page and Back Button Issues

## Implementation Tasks

1.  **Modify `ReservationCreateProxyView.post`**
    - [x] Create a `legacy_payload` by copying `request.data`.
    - [x] Apply field mapping:
        - `flightNumber` -> `flight_number`
        - `notes` -> `comments`
        - `firstName` -> `first_name`
        - `lastName` -> `last_name`
        - `email` -> `email_address`
    - [x] Update reservation creation to use `legacy_payload`.
    - [x] Remove `to_relative` helper and absolute-to-relative path conversion logic.
    - [x] Pass `success_url` and `cancel_url` from `request.data` directly to `fetch_payment_link`.
    - [x] Add logic to hoist `paypal_id` from `link_data` to the top-level response payload.

2.  **Verify consistent "CASH" response**
    - [x] Ensure `CASH` response includes `reservation_id`, `uuid`, `payment_method`, and `payment_data`.

## Validation Tasks

1.  **Unit Tests**
    - [x] Add a test case to `legacy_middleware/tests/test_views.py` to verify field mapping in `ReservationCreateProxyView`.
    - [x] Add a test case to verify absolute URLs are used for payment links.
    - [x] Add a test case to verify `paypal_id` is hoisted to the top level.
    - [x] Add a test case to verify `CASH` response structure.

2.  **Manual Verification**
    - [x] Verify using the local dev server and mock responses that the changes work as expected.
