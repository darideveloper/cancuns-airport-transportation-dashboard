# Proposal: Fix After-Payment Page and Back Button Issues

This proposal addresses several issues in the `ReservationCreateProxyView` to improve frontend integration and fix critical bugs related to payment provider redirects.

## Problem Statement

The current implementation of `ReservationCreateProxyView` has three main issues:
1.  **Relative Redirect URLs:** Absolute URLs provided by the frontend are converted to relative paths before being sent to the legacy payment API. Payment providers like PayPal and Stripe require absolute URLs for redirects.
2.  **Field Mismatch:** The frontend sends field names (e.g., `flight_number`, `firstName`) that the legacy API does not recognize, leading to missing data in reservations.
3.  **Nested Payment Data:** Some crucial fields like `paypal_id` are nested within `payment_data`, making it harder for the frontend to access them.

## Proposed Changes

### 1. Maintain Absolute Redirect URLs
Remove the `to_relative` helper and pass the `success_url` and `cancel_url` from the request directly to the `fetch_payment_link` service.

### 2. Implement Field Mapping
Introduce a mapping layer in `ReservationCreateProxyView.post` to translate frontend field names to the legacy API's expected field names.
- `flight_number` -> `flight`
- `notes` -> `comments`
- `firstName` -> `first_name`
- `lastName` -> `last_name`
- `email` -> `email_address`

### 3. Hoist `paypal_id` to Top Level
If the legacy payment API returns a `paypal_id`, include it at the top level of the JSON response payload.

### 4. Ensure Consistent Response for CASH
Verify that the response for `CASH` payment method remains consistent with online payment responses (containing `reservation_id`, `uuid`, `payment_method`, and an empty `payment_data` object).

## Impact

- **Reliability:** Fixes the redirect issue with payment providers.
- **Data Integrity:** Ensures all reservation details (flight, name, notes) are correctly recorded in the legacy system.
- **Frontend Simplicity:** Reduces the logic required on the frontend to handle different payment responses.
