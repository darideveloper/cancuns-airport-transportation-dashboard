# Design: Fix PayPal ID Hoisting Key

## Overview
This design clarifies the logic to correctly hoist the PayPal Order ID from the legacy API response.

## Component Changes

### 1. `ReservationCreateProxyView` (in `legacy_middleware/views.py`)

#### Improved Hoisting Logic
When the payment provider is `PAYPAL-V2`, the legacy system returns the PayPal Order ID in the `url` field. We will prioritize the `paypal_id` field if it exists, but fallback to `url` specifically for `PAYPAL-V2`.

```python
# After parsing link_data
response_payload = {
    "reservation_id": reservation_id,
    "uuid": uuid,
    "payment_method": original_payment_method,
    "payment_data": link_data
}

# Hoist paypal_id if present with safety check and provider-specific fallback
if isinstance(link_data, dict):
    if "paypal_id" in link_data:
        response_payload["paypal_id"] = link_data["paypal_id"]
    elif payment_provider == "PAYPAL-V2" and "url" in link_data:
        # For PAYPAL-V2, 'url' field contains the actual Order ID
        response_payload["paypal_id"] = link_data["url"]
```

## Considerations
- **Specific Provider Targeting:** Only applying the `url` fallback to `PAYPAL-V2` prevents misidentifying Stripe's actual checkout URL as a PayPal ID.
