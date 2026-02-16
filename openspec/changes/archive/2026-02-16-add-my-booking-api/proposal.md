# Change: Add "My Booking" Retrieval API

## Why
Customers need to retrieve their existing booking details to view reservation status, manage changes, or access payment information without exposing legacy API credentials to the frontend.

## What Changes
- Add new `MyBookingProxyView` to the legacy_middleware app
- Implement `fetch_my_booking` service function for booking retrieval
- Add new URL endpoint `/legacy/my-booking/` for booking retrieval
- Create comprehensive tests for the new endpoint
- Follow existing middleware patterns for credential hiding and error handling

## Impact
- Affected specs: New `my-booking-api` capability
- Affected code: `legacy_middleware/views.py`, `legacy_middleware/services.py`, `legacy_middleware/urls.py`, `legacy_middleware/tests/`
