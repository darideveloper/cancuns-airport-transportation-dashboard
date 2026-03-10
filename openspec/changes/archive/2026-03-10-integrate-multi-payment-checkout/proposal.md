# Proposal: Integrate Multi-Payment Checkout (PayPal SDK, Card, Cash)

## Problem Statement
The current checkout system in the Django middleware only supports redirect-based payments for Stripe and PayPal, returning a single `payment_link`. This prevents the Astro frontend from using the modern PayPal JavaScript SDK for an "in-app" checkout experience. Additionally, the system needs to explicitly support `CASH` as a first-class payment option and map `CREDIT_CARD` to PayPal's infrastructure.

## Proposed Solution
Update the `legacy_middleware` to:
1.  Support a hybrid PayPal flow where the middleware provides the `paypal_id` (Order ID) and other metadata for the frontend SDK.
2.  Map `CREDIT_CARD` payment requests to the `PAYPAL` provider.
3.  Add a new `/legacy/capture/` endpoint to finalize PayPal transactions from the frontend.
4.  Ensure `CASH` payments return full reservation details immediately.

## Key Features
- **PayPal SDK Metadata**: Success responses for PayPal/Card will include `paypal_id`, `reservation_id`, and `uuid`.
- **Payment Mapping**: `CREDIT_CARD` is internally treated as `PAYPAL`.
- **Capture API**: Proxy to the legacy capture endpoint.
- **Improved Cash Flow**: Consistent handling of non-digital payments.

## Relationship to Existing Specs
- **MODIFIES** `reservation-proxy`: Updates the response structure for online payments and adds capture requirements.
- **ADDS** `reservation-proxy`: Adds the Capture API requirement.
