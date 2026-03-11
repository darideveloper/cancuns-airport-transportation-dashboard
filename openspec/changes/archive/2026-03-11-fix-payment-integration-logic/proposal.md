# Proposal: Fix Payment Integration Logic

## Summary
Improve the payment integration in the legacy middleware API by:
1. Adding the required `pay_at_arrival: 1` flag for Cash reservations.
2. Updating the PayPal provider type to `PAYPAL-V2` for modern SDK support.
3. Standardizing the response structure across all payment methods.
4. Preserving the original payment method selection (e.g., `CREDIT_CARD`) in the API response.

## Motivation
The current implementation fails to correctly identify Cash reservations in the legacy backend due to the missing `pay_at_arrival` flag. Additionally, the PayPal integration uses an older provider type (`PAYPAL`) instead of the required `PAYPAL-V2`, which may cause issues with modern checkout SDKs. The response structure is also inconsistent between cash and online payments, making it harder for the frontend to handle.

## Proposed Changes

### Logic Improvements
- **Cash Reservations:** When `payment_method` is `"CASH"`, the system will inject `"pay_at_arrival": 1` into the payload sent to the legacy backend. For all other methods, this key will be omitted.
- **PayPal Provider:** The `type` parameter sent to the legacy payment handler for PayPal will be changed from `PAYPAL` to `PAYPAL-V2`.
- **Payment Method Preservation:** The middleware will keep track of the original `payment_method` (e.g., `CREDIT_CARD`) and return it in the response, even if it was mapped to `PAYPAL` for the upstream call.
- **URL Handling:** Ensure `cancel_url` and `success_url` are properly handled to avoid path doubling when generating payment links.

### Response Standardization
All successful reservation creations will return a consistent JSON structure:
- `reservation_id`: The ID from the legacy system.
- `uuid`: The unique UUID for the reservation.
- `payment_method`: The original method selected (e.g., `CASH`, `PAYPAL`, `CREDIT_CARD`).
- `payment_data`: A dictionary containing all metadata from the payment provider (e.g., `paypal_order_id`, `stripe_url`).

### Safety & Error Handling
- **502 Bad Gateway Mapping:** Improve error mapping when upstream responses are malformed or the payment provider fails.
- **Atomic Operations:** Ensure that if payment link generation fails, the error message returned to the user is descriptive enough to avoid duplicate reservation attempts where possible.

## Impact
- **Backend (Middleware):** Updates to `ReservationCreateProxyView` and `fetch_payment_link`.
- **Legacy API:** No changes (this fix aligns the middleware with existing Legacy API requirements).
- **Frontend:** Improved consistency and correct handling of Cash/PayPal flows.
