# Tasks

- [x] **Refactor `_post_to_legacy`** <!-- id: 1 -->
  - File: `legacy_middleware/services.py`
  - Rename `_post_to_legacy` to `_legacy_req` (or add logic) to support `method` argument for GET requests.
  - Update all existing calls to use the new signature or method.

- [x] **Implement `fetch_payment_link` Service** <!-- id: 2 -->
  - File: `legacy_middleware/services.py`
  - Create `fetch_payment_link(token, reservation_id, payment_provider, language, success_url, cancel_url)`.
  - Use `_legacy_req` with `GET` method and query params.

- [x] **Update `ReservationCreateProxyView` Logic** <!-- id: 3 -->
  - File: `legacy_middleware/views.py`
  - In `post` method, after successful creation:
    - Check `payment_method` in request data.
    - If "STRIPE" or "PAYPAL":
      - Extract `reservation_id` from initial response.
      - Call `fetch_payment_link`.
      - Return `Response({"payment_link": ...})`.
    - Else: return original response.

- [x] **Update `ReservationCreateProxyView` Validation** <!-- id: 4 -->
  - Ensure `extract_reservation_id` logic robustly handles nested `config.id` or root `id` structures often seen in legacy responses.

- [x] **Add Tests for Payment Link Generation** <!-- id: 5 -->
  - File: `legacy_middleware/tests/test_views.py`
  - Implement `test_create_success_stripe`: Verify JSON response `{ "payment_link": "..." }`.
  - Implement `test_create_success_paypal`: Verify JSON response `{ "payment_link": "..." }`.
  - Implement `test_create_payment_link_failure`: Verify 502 status.
  - Implement `test_create_cash_ignored`: Verify standard reservation response.

- [x] **Update Service Tests for Refactor** <!-- id: 6 -->
  - File: `legacy_middleware/tests/test_services.py`
  - Update existing tests to mock `requests.request` (or `get`/`post`) as per new implementation.
  - Add `test_fetch_payment_link` to verify URL and params construction.
