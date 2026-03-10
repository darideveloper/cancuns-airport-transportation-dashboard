# Design: Multi-Payment Checkout (SDK, Card, Cash)

## Architecture Overview
The system moves from a "Redirect-Only" flow to a "Hybrid SDK/Redirect" flow to allow the Astro frontend to render the PayPal SDK.

### Current Flow (Redirect)
1.  User selects payment method (PayPal/Stripe).
2.  Django calls Legacy API to create reservation.
3.  Django calls Legacy API to get a `payment_link`.
4.  Django returns `payment_link`.
5.  Frontend redirects user to the link.

### New Flow (SDK-based)
1.  User selects "PayPal Account" or "Credit Card".
2.  Astro frontend POSTs to Django `/legacy/create/`.
3.  Django creates the reservation and calls the payment handler.
4.  Django returns `paypal_id` (the PayPal Order ID) + `reservation_id` + `uuid` + `payment_link` (as fallback).
5.  Astro frontend initializes the PayPal SDK with `paypal_id`.
6.  User approves the payment.
7.  Astro frontend POSTs to Django `/legacy/capture/` with the Order ID.
8.  Django calls the Legacy API capture endpoint and returns the status.

## Decision: Mapping `CREDIT_CARD` to `PAYPAL`
The legacy system expects `type=PAYPAL` for both PayPal accounts and card payments processed via PayPal's SDK. To simplify the frontend selection:
- Frontend can send `payment_method: "CREDIT_CARD"`.
- Middleware maps this to `PAYPAL` before calling the legacy system.
- This allows the frontend to distinguish the user's intent while the backend stays compatible with the legacy API.

## Decision: Enhanced Response Structure
Returning the full JSON from the legacy payment handler ensures the middleware remains decoupled from the specific fields returned by the upstream API (like `paypal_id`).

## Decision: Dedicated Capture Endpoint
Adding `/legacy/capture/` provides a secure, authenticated channel for the frontend to finalize transactions without exposing the Legacy API directly.
