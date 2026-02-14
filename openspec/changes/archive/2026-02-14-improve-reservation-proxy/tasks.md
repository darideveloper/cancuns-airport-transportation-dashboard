# Tasks: Improve Reservation Proxy View

## View Layer
- [x] Add `validate_reservation_response` method to `ReservationCreateProxyView` in `legacy_middleware/views.py` to:
    - [x] Check that response data is a dictionary (type safety).
    - [x] Pass through application-level errors (responses with `"error"` key).
    - [x] Verify presence of `reservation_id` or `id` in success responses.
- [x] Update `post` method in `ReservationCreateProxyView` to use the validation function.

## Service Layer
- [x] Create `legacy_middleware/tests/test_services.py` to test service functions directly:
    - [x] `test_fetch_reservation_create_injects_site_id`: Verify `site_id` is injected from settings when missing.
    - [x] `test_fetch_reservation_create_preserves_site_id`: Verify existing `site_id` in payload is not overwritten.
    - [x] `test_fetch_reservation_create_auth_header`: Verify correct `Authorization: Bearer <token>` header is sent.
    - [x] `test_fetch_quote_injects_rate_group`: Verify `rate_group` is injected from settings when missing (bonus cleanup).

## View Tests
- [x] Create `ReservationCreateProxyViewTestCase` in `legacy_middleware/tests/test_views.py` with the following tests:
    - [x] `test_create_success`: Verify 200 OK and valid JSON response.
    - [x] `test_create_validation_error`: Verify 422 Bad Request is forwarded correctly.
    - [x] `test_token_refresh_retry`: Verify 401 triggers token refresh and retry.
    - [x] `test_upstream_failure`: Verify 500/connection error returns 502 Bad Gateway.
    - [x] `test_malformed_response_non_dict`: Verify non-dictionary responses return 502.
    - [x] `test_malformed_response_missing_id`: Verify 200 OK without `reservation_id`/`id` returns 502.

## Integration Tests
- [x] Create `ReservationCreateProxyLiveTests` class in `legacy_middleware/tests/test_views.py` marked with `@tag("integration")` and skipped unless `LIVE_API_TESTS` env var is set.
    - [x] `test_create_live_success`: Verify real creation flow with valid payload (may require fetching quote details first).

