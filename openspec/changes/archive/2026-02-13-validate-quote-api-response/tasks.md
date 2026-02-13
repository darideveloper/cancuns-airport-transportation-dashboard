# Tasks: Validate Quote API Response

- [x] **Task 1: Update and Expand Tests**
  - Update `legacy_middleware/tests/test_views.py`:
    - Rename/Refactor `test_view_happy_path_no_token` to include `items` and `places` in mock response.
    - Add `test_view_no_availability`: Verify `200 OK` with `error` object is PASSED THROUGH.
    - Add `test_view_malformed_response`: Verify `502` when `items` or `places` is missing in successful 200 response.
  - Verify `QuoteProxyLiveTests` passes (ensure live API returns `places` or adjust validation if necessary).
  - Verification: `python manage.py test legacy_middleware.tests.test_views`

- [x] **Task 2: Implement Validation Logic**
  - Update `QuoteProxyView.post` in `legacy_middleware/views.py`.
  - Check for `error` key in 200 response -> return as is.
  - Else, check for `items` (list) AND `places` (dict).
  - If missing/invalid -> return 502 with error message.
  - Ensure 422 responses fall through naturally.
  - Verification: Run updated tests.

- [x] **Task 3: Refactor Common Test Helpers (Optional)**
  - Skipped: Repetition is low enough to maintain readability without abstraction.
