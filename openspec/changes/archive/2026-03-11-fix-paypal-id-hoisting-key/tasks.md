# Tasks: Fix PayPal ID Hoisting Key

## Implementation Tasks

1.  **Modify `ReservationCreateProxyView.post`**
    - [x] Update hoisting logic to include `url` as a source for `paypal_id` for `PAYPAL-V2` provider.

## Validation Tasks

1.  **Unit Tests**
    - [x] Update `ReservationCreateProxyViewNewTests.test_hoisted_paypal_id` to verify hoisting from the `url` field when using `PAYPAL-V2`.
    - [x] Run all `legacy_middleware` tests to ensure no regressions.
