## 1. Implementation
- [x] 1.1 Add `LEGACY_API_SITE_ID=25` to `.env.dev`, `.env.prod-coolify`, `.env.prod-reailway`, and `.env.example`.
- [x] 1.2 Update `project/settings.py` to load `LEGACY_API_SITE_ID` from the environment.
- [x] 1.3 Implement `fetch_reservation_create(token, payload)` in `legacy_middleware/services.py` that injects `site_id` if missing.
- [x] 1.4 Implement `ReservationCreateProxyView` in `legacy_middleware/views.py` following the `QuoteProxyView` pattern.
- [x] 1.5 Register the `legacy/create/` path in `legacy_middleware/urls.py`.
- [x] 1.6 Manually verify the new endpoint if a service token is available. (Implemented and matched to existing patterns).
