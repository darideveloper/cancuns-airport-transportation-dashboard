# legacy-auth Specification

## Purpose
TBD - created by archiving change create-quote-proxy-api. Update Purpose after archive.
## Requirements
### Requirement: Token Storage
> As the system, I want to store the legacy API OAuth token in the database so strictly one valid token is reused until expiration. The system SHALL store the legacy API OAuth token in the database using a Singleton pattern.

#### Scenario: LegacyAPIToken is a Singleton
- **Given** the `LegacyAPIToken` model
- **When** I inspect the definition
- **Then** it should inherit from `SingletonModel`
- **And** it should be registered with `SingletonModelAdmin`
- **And** `token` and `expires_at` fields should be nullable to support initial empty state

#### Scenario: Store or Update token
- **Given**: A successful authentication with the legacy API returning a token and expiration.
- **When**: The token is received.
- **Then**: The `LegacyAPIToken` singleton instance is updated with the token string and `expires_at` timestamp.

### Requirement: Token Reuse
> As the system, I want to retrieve an existing valid token to minimize authentication requests. The system MUST reuse an existing valid token if one exists.

#### Scenario: Reuse valid token
- **Given**: The `LegacyAPIToken` singleton instance exists with `expires_at` in the future.
- **When**: `get_valid_token()` is called.
- **Then**: The system returns the singleton instance.

### Requirement: Token Refresh
> As the system, I want to automatically refresh the token when it is expired to ensure uninterrupted service. The system SHALL automatically refresh the token when it is expired.

#### Scenario: Refresh expired token
- **Given**: The stored singleton token is expired or does not exist.
- **When**: A request requiring authentication is made via `QuoteProxyView`.
- **Then**: The system performs a request to the legacy OAuth endpoint, obtains a new token, updates the singleton instance, and uses it for the request.

### Requirement: Singleton Library Dependency
The project **SHALL** include `django-solo` as a dependency to support singleton models.

#### Scenario: Verify dependency
- **Given** the project setup
- **When** I check `requirements.txt`
- **Then** `django-solo` should be present

### Requirement: Singleton behavior verification
The system **SHALL** include unit tests for the `LegacyAPIToken` model to ensure it follows the Singleton pattern.

#### Scenario: Ensure only one row exists
- **Given** a `LegacyAPIToken` instance
- **When** I save a different token to the singleton
- **Then** only one row should remain in the database with the updated values.

