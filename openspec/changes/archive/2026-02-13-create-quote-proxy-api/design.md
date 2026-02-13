# Design: Quote Proxy Authentication

To securely access the legacy API's protected endpoints (Quote/Search), we implement a token management strategy within the Django backend. This avoids exposing credentials to the client.

## Components

### 1. Token Storage (`LegacyAPIToken`)
A simple Django model acting as a persistent cache for the OAuth token.
- **Fields**:
  - `token`: Encrypted or plain text token string (since it's internal middleware, plain text is acceptable for MVP but encrypted is safer). For this proposal, we use `TextField`.
  - `expires_at`: Calculated expiration time (typically `now + expires_in - buffer`).
  - `created_at`: Creation timestamp.

### 2. Token Lifecycle Management
The view `QuoteProxyView` acts as the orchestrator.
- **Lazy Loading**: Check for a valid token in the DB before making a request.
- **Refresh Strategy**: If no valid token exists (or is expired), perform login (`fetch_legacy_token`), save the new token, then proceed.
- **Race Conditions**: For low traffic, simple check-then-act is sufficient. For high traffic, we might need a lock or just let requests race (resulting in a few extra token fetches, which is usually harmless for OAuth).

### 3. Middleware Workflow
1.  **Frontend Request**: `POST /legacy/quote/` (Public, no auth required).
2.  **Backend Check**:
    - `token = LegacyAPIToken.objects.filter(expires_at__gt=now).last()`
    - If `!token`:
        - `auth_response = post(LEGACY_API_URL + '/oauth', auth=(user, pass))`
        - `token = save(auth_response)`
3.  **Upstream Request**:
    - `response = post(LEGACY_API_URL + '/quote', headers={'Authorization': f'Bearer {token.token}'}, json=request.data)`
4.  **Response**: Return upstream JSON directly to frontend.

### 4. Configuration
Credentials are loaded from environment variables to ensure security and flexibility across environments.
- `LEGACY_API_USER`
- `LEGACY_API_SECRET`
