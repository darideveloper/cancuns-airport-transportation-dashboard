# Tasks: Refactor Legacy Middleware for DRY

## Phase 1: Service Refactoring
- [x] Create `_post_to_legacy` helper in `legacy_middleware/services.py`.
- [x] Refactor `fetch_quote` to use the helper.
- [x] Refactor `fetch_reservation_create` to use the helper.
- [x] Verify that services still inject their respective default fields (`rate_group` and `site_id`).

## Phase 2: View Infrastructure
- [x] Implement `BaseLegacyProxyView` in `legacy_middleware/views.py`.
    - [x] Add `get_legacy_token` method.
    - [x] Add `execute_proxy_request` method with 401 retry logic and centralized error handling.
- [x] Refactor `QuoteProxyView` to inherit from `BaseLegacyProxyView` and use `execute_proxy_request`.
- [x] Refactor `ReservationCreateProxyView` to inherit from `BaseLegacyProxyView` and use `execute_proxy_request`.

## Phase 3: Cleanup and Validation
- [x] Refactor `AutocompleteProxyView` if applicable (it doesn't use JWT, but could use centralized error handling).
- [x] Remove redundant `try/except` and token refresh blocks from individual views.
- [x] Run current tests to ensure no regressions in proxy functionality.
- [x] (Optional) Add a simple unit test to verify `BaseLegacyProxyView` correctly handles retries.
