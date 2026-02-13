# autocomplete-proxy Specification

## Purpose
TBD - created by archiving change create-legacy-autocomplete-proxy. Update Purpose after archive.
## Requirements
### Requirement: Legacy Autocomplete Proxy

The system SHALL act as a secure proxy for the legacy `autocomplete-affiliates` endpoint, hiding the `app-key` from the public client.

#### Scenario: Successful Location Search
Given the backend is configured with a valid `LEGACY_API_KEY`
And the external legacy API is operational
When a `POST` request is made to `/api/legacy/autocomplete/` with `{"keyword": "cancun"}`
Then the system sends a request to the legacy API with the configured `app-key`
And the system returns a `200 OK` response containing the JSON list of items from the legacy API
And the response DOES NOT contain the `app-key`

#### Scenario: Missing Keyword
When a `POST` request is made to `/api/legacy/autocomplete/` with an empty body or `{"keyword": ""}`
Then the system returns a `400 Bad Request` error
And the system DOES NOT make a request to the legacy API

#### Scenario: Legacy API Failure
Given the legacy API is down or returning `500 Internal Server Error`
When a `POST` request is made to `/api/legacy/autocomplete/` with `{"keyword": "cancun"}`
Then the system returns a `502 Bad Gateway` (or `503 Service Unavailable`) error
And the error response indicates an upstream failure

#### Scenario: Legacy API Validation Error
Given the legacy API returns a `422 Unprocessable Entity` (e.g., keyword too short)
When a `POST` request is made to `/api/legacy/autocomplete/` with a short keyword
Then the system returns the same status code and error message from the legacy API to the client

### Requirement: Live API Integration Verification
The system SHALL provide a way to verify the autocomplete proxy against the live legacy API in controlled environments.

#### Scenario: Live Autocomplete Success
- **Given**: The system is configured with valid live credentials.
- **And**: `LIVE_API_TESTS` is enabled.
- **When**: A search request is made to the real legacy API via the proxy.
- **Then**: It MUST return a 200 OK with actual location data.

