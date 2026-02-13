## ADDED Requirements

### Requirement: Token Storage
> As the system, I want to store the legacy API OAuth token in the database so strictly one valid token is reused until expiration. The system SHALL store the legacy API OAuth token in the database.

#### Scenario: Store new token
- **Given**: A successful authentication with the legacy API returning a token and expiration.
- **When**: The token is received.
- **Then**: A `LegacyAPIToken` record is created or updated with the token string and calculated `expires_at` timestamp.

### Requirement: Token Reuse
> As the system, I want to retrieve an existing valid token to minimize authentication requests. The system MUST reuse an existing valid token if one exists.

#### Scenario: Reuse valid token
- **Given**: A valid `LegacyAPIToken` exists in the database with `expires_at` in the future.
- **When**: A request requiring authentication is made.
- **Then**: The system retrieves the existing token from the database instead of requesting a new one.

### Requirement: Token Refresh
> As the system, I want to automatically refresh the token when it is expired to ensure uninterrupted service. The system SHALL automatically refresh the token when it is expired.

#### Scenario: Refresh expired token
- **Given**: The stored token is expired or does not exist.
- **When**: A request requiring authentication is made.
- **Then**: The system performs a request to the legacy OAuth endpoint, obtains a new token, saves it, and uses it for the request.
