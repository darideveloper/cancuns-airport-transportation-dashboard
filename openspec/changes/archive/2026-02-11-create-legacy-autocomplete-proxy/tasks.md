# Tasks

- [x] Add `LEGACY_API_BASE_URL` and `LEGACY_API_KEY` to `.env.example` and load them in `project/settings.py`. <!-- id: 0 -->
- [x] Create `legacy_middleware/services.py` (or similar) with a client/function to query the legacy autocomplete API. Ensure it uses `requests` and handles timeouts/errors. <!-- id: 1 -->
- [x] Create `AutocompleteProxyView` in `legacy_middleware/views.py`. This view should accept POST requests, validate the body, call the service, and return the response. <!-- id: 2 -->
- [x] Register the new view in `legacy_middleware/urls.py` and include it in `project/urls.py` under `api/legacy/` (or strictly following the existing `api/` router if preferred, but a custom path might be cleaner for this proxy). <!-- id: 3 -->
- [x] Create `legacy_middleware/tests/` directory and `__init__.py`. <!-- id: 8 -->
- [x] Write `test_autocomplete_success` in `legacy_middleware/tests/test_views.py`: Mock the external API to return a standard list of locations and verify the Django view returns 200 OK with the same JSON. <!-- id: 4 -->
- [x] Write `test_autocomplete_validation` in `legacy_middleware/tests/test_views.py`: Send a request without `keyword` and verify 400 Bad Request. <!-- id: 5 -->
- [x] Write `test_autocomplete_external_error` in `legacy_middleware/tests/test_views.py`: Mock the external API to raise a connection error or return 500, and verify the Django view returns an appropriate error (e.g., 502 or 503). <!-- id: 6 -->
- [x] Verify env variables are correctly pulled from settings in the service (test configuration). <!-- id: 7 -->
