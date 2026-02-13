# Create Quote Proxy API

## Summary
Implement a middleware API `QuoteProxyView` that proxies requests to the legacy "Quote/Search" endpoint. This middleware will handle authentication internally by managing a persistent OAuth token stored in the database, effectively hiding the legacy API's authentication complexity from the frontend.

## Motivation
The legacy API requires an OAuth token for the Quote/Search endpoint. Exposing the user/password credentials to the frontend to obtain this token is insecure. A middleware approach allows the backend to securely manage credentials and tokens, acting as a transparent proxy for the frontend.

## Proposed Changes
1.  **Database Model**: Create `LegacyAPIToken` model to store authentication tokens and their expiration.
2.  **Service Layer**:
    *   Implement `fetch_legacy_token` to authenticate with the legacy API.
    *   Implement `fetch_quote` to call the legacy Quote endpoint using the stored token.
3.  **Views**: Create `QuoteProxyView` to handle frontend requests, manage token lifecycle (fetch/refresh), and proxy the request to the upstream API.
4.  **Configuration**: Add necessary environment variables (`LEGACY_API_USER`, `LEGACY_API_SECRET`) to `.env` and `settings.py`.

## Governance
- **Rely on**: `legacy_middleware/docs/legacy-api.md` for endpoint specifications.
- **Validation**: Ensure strict separation of concerns; frontend receives data without knowing about upstream auth.
