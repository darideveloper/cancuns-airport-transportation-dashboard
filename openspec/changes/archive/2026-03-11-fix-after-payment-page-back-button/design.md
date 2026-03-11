# Design: Fix After-Payment Page and Back Button Issues

## Overview
This design clarifies the updates to `ReservationCreateProxyView` to improve frontend compatibility and fix critical redirect issues with payment providers.

## Component Changes

### 1. `ReservationCreateProxyView` (in `legacy_middleware/views.py`)

#### Field Mapping
The frontend uses field names that align with modern web standards, but the legacy API requires different keys. We will implement a mapping layer before sending the payload to the legacy system.

```python
# Mapping before sending to legacy API
legacy_payload = payload.copy()

mapping = {
    "flight_number": "flight",
    "flightNumber": "flight",
    "notes": "comments",
    "firstName": "first_name",
    "lastName": "last_name",
    "email": "email_address"
}

for front_key, back_key in mapping.items():
    if front_key in legacy_payload:
        legacy_payload[back_key] = legacy_payload.pop(front_key)
```

#### Absolute Redirect URLs
The `to_relative` helper function currently strips domains from `success_url` and `cancel_url`. This is a bug for payment providers that expect an absolute return address. We will remove the `to_relative` function definition and its usage.

```python
# Use absolute URLs directly
success_val = request.data.get("success_url")
cancel_val = request.data.get("cancel_url")
```

#### Hoisted `paypal_id`
To simplify frontend parsing, if `paypal_id` is present in the `payment_data` returned from the legacy API, we will hoist it to the top level of the response.

```python
# After link_data = payment_response.json()
response_payload = {
    "reservation_id": reservation_id,
    "uuid": uuid,
    "payment_method": original_payment_method,
    "payment_data": link_data
}

# Hoist paypal_id if present with safety check
if isinstance(link_data, dict) and "paypal_id" in link_data:
    response_payload["paypal_id"] = link_data["paypal_id"]

return Response(response_payload, status=status.HTTP_200_OK)
```

## Considerations
- **Backward Compatibility:** These changes are additive or corrective, ensuring the frontend receives a more predictable and feature-complete response.
- **Data Integrity:** By mapping fields correctly, we prevent data loss when creating reservations in the legacy system.
