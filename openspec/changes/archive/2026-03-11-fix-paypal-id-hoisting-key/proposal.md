# Proposal: Fix PayPal ID Hoisting Key

This proposal fixes a bug where `paypal_id` is missing from the top level of the reservation creation response when using the modern PayPal provider.

## Problem Statement

The current implementation of `ReservationCreateProxyView` only looks for a field named `paypal_id` to hoist to the top level. However, the legacy API for `PAYPAL-V2` (modern PayPal SDK) returns the Order ID in a field named `url`. This causes the frontend to miss the ID required to initialize the PayPal buttons.

## Proposed Changes

### 1. Update Hoisting Logic
Modify `ReservationCreateProxyView.post` to check for `url` as a source for `paypal_id` specifically when the payment provider is `PAYPAL-V2`.

```python
if isinstance(link_data, dict):
    if "paypal_id" in link_data:
        response_payload["paypal_id"] = link_data["paypal_id"]
    elif payment_provider == "PAYPAL-V2" and "url" in link_data:
        response_payload["paypal_id"] = link_data["url"]
```

## Impact

- **Reliability:** Ensures the frontend correctly receives the PayPal Order ID.
- **Frontend Compatibility:** Matches the expectations set in `docs/after-payment-page-fix-front.md`.
