# Tasks

1. Create Model `LegacyAPIToken`

   - [x] Add `token` (TextField) to store the oauth token.
   - [x] Add `expires_at` (DateTimeField) to store token expiration.
   - [x] Add `created_at` (DateTimeField) for audit.
   - [x] Implement query methods to fetch valid token or return None.
2. Environment Configuration

   - [x] Add `LEGACY_API_USER` to `.env` and `settings.py`.
   - [x] Add `LEGACY_API_SECRET` to `.env` and `settings.py`.
   - [x] Add `LEGACY_API_SITE_ID` to `.env` and `settings.py`.
   - [x] Add `LEGACY_API_RATE_GROUP` to `.env` and `settings.py`.
3. Implement Service Logic

   - [x] Create `fetch_legacy_token()` in `legacy_middleware/services.py` to:
     - POST to `/api/v1/oauth`.
     - Handle errors and return token + expiry.
   - [x] Create `fetch_quote(token, ...)` in `legacy_middleware/services.py` to:
     - POST to `/api/v1/quote`.
     - Use `Authorization: Bearer <token>`.
     - Pass through request body.
4. Implement `QuoteProxyView`

   - [x] Create `QuoteProxyView` in `legacy_middleware/views.py`.
   - [x] On POST request:
     - Check if valid token exists in `LegacyAPIToken`.
     - If expired/missing, call `fetch_legacy_token()` and save new `LegacyAPIToken`.
     - Call `fetch_quote()` with the valid token.
     - Return the response to the frontend.
   - [x] Handle upstream errors gracefully (401, 502, etc.).
5. Register URL

   - [x] Add `path('legacy/quote/', QuoteProxyView.as_view(), name='legacy_quote')` to `legacy_middleware/urls.py`.
6. Testing

   - [x] Create `legacy_middleware/tests_quote.py` using `APITestCase`.
   - [x] **Test: Model Constraints**
     - Verify `LegacyAPIToken` stores token and expiry correctly.
   - [x] **Test: Service Fetch Token (Mocked)**
     - Mock upstream `oauth` endpoint success -> assert logic returns token.
     - Mock upstream `oauth` failure -> assert logic raises exception.
   - [x] **Test: View - Happy Path (No Token)**
     - Start with empty DB.
     - Mock `oauth` success + `quote` success.
     - POST to `/legacy/quote/`.
     - Verify `LegacyAPIToken` is created.
     - Verify response matches mock quote data.
   - [x] **Test: View - Happy Path (Reuse Token)**
     - Pre-fill `LegacyAPIToken` with valid future expiry.
     - Mock `quote` success (assert `oauth` is NOT called).
     - POST to `/legacy/quote/`.
     - Verify response matches mock quote data.
   - [x] **Test: View - Expired Token Auto-Refresh**
     - Pre-fill `LegacyAPIToken` with past expiry.
     - Mock `oauth` success + `quote` success.
     - POST to `/legacy/quote/`.
     - Verify `oauth` was called.
     - Verify `LegacyAPIToken` is updated with new token.
   - [x] **Test: View - Upstream Error Handling**
     - Mock `quote` returning 422 (validation error).
     - POST to `/legacy/quote/`.
     - Verify proxy returns 422 and upstream error message.
   - [x] **Test: View - Upstream Auth Failure (Edge Case)**
     - Pre-fill valid token.
     - Mock `quote` returning 401.
     - Verify proxy returns 401 or implementing retry logic (optional but good).
