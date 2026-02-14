## Context
We are adding a third proxy endpoint to `legacy_middleware`. The previous ones (`AutocompleteProxyView`, `QuoteProxyView`) share some logic, specifically token management and error handling.

## Goals
- Add `POST /legacy/create/`.
- Ensure `site_id` (always 25) is injected.
- Reuse `LegacyAPIToken` logic (DRY).
- Maintain consistent error handling (forwarding 422, status codes, and 502 for upstream failures).

## Decisions
- **Inject `site_id` in `fetch_reservation_create`**: Similar to how `rate_group` is injected in `fetch_quote`. The `site_id` will be fetched from `settings.LEGACY_API_SITE_ID`.
- **View Pattern**: Follow `QuoteProxyView` structure for token acquisition, response parsing, and retry logic on 401.

## Risks / Trade-offs
- **Duplicate Logic**: While we follow the pattern, we are duplicating some view-level logic (token retrieval and retry). Given the limited number of endpoints, this is acceptable compared to introducing an abstract base class that might complicate simple proxying.
- **Site ID Source**: Even though it's always 25, we use an env variable for flexibility as requested.
