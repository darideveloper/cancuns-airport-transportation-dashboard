# Change: Add Reservation Proxy Endpoint

## Why
The project needs to allow users to create a new booking with customer details by proxying requests to the legacy API. This should follow the same pattern as existing proxy endpoints (Autocomplete and Quote) while maintaining DRY principles for authentication and configuration.

## What Changes
- Add `LEGACY_API_SITE_ID` configuration to `settings.py` (loading from `.env`, defaulting to 25).
- Implement `fetch_reservation_create` in `services.py` to handle the upstream API call.
- Create `ReservationCreateProxyView` in `views.py` with automatic JWT token management and default `site_id` injection.
- Register `POST /legacy/create/` endpoint in `urls.py`.

## Impact
- Affected specs: `reservation-proxy` (New capability)
- Affected code: `legacy_middleware/views.py`, `legacy_middleware/services.py`, `legacy_middleware/urls.py`, `project/settings.py`
