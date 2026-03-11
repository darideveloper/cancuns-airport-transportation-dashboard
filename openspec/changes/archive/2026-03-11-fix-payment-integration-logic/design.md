# Design: Payment Integration Logic Fixes

## Overview
This design improves the interaction between the middleware and the legacy API's reservation and payment endpoints. It addresses inconsistencies in parameter mapping and response formats.

## Architecture & Flows

### 1. Cash Payment Logic
The middleware must act as a logic injector for the legacy `POST /api/v1/create` endpoint.
- **Input:** `payment_method: "CASH"`.
- **Logic:** Add `pay_at_arrival: 1` to the legacy payload.
- **Logic:** Omit `pay_at_arrival` if `payment_method != "CASH"`.

### 2. PayPal provider (V2)
The legacy `GET /api/v1/reservation/payment/handler` endpoint requires `type=PAYPAL-V2` for modern PayPal Checkout integrations.
- **Mapping:**
  - `PAYPAL` -> `PAYPAL-V2`
  - `CREDIT_CARD` -> `PAYPAL-V2`

### 3. Response Standardization
The API response structure currently differs between payment methods. We will standardize it to ensure the frontend always receives the same fields.

**Current Response (Cash):**
```json
{
  "id": 123,
  "uuid": "...",
  "status": "pending"
}
```

**Current Response (PayPal):**
```json
{
  "payment_link": "ORDER_ID",
  "reservation_id": 123,
  "uuid": "...",
  "paypal_id": "...",
  "url": "ORDER_ID"
}
```

**Standardized Response (All):**
```json
{
  "reservation_id": 123,
  "uuid": "...",
  "payment_method": "CASH",
  "payment_data": {
    "payment_link": "...",
    "paypal_order_id": "...",
    "url": "..."
  }
}
```

## Traceability
This change modifies `ReservationCreateProxyView.post` in `legacy_middleware/views.py` and `fetch_payment_link` in `legacy_middleware/services.py`.
It updates the `reservation-proxy` spec to reflect these refined requirements.
