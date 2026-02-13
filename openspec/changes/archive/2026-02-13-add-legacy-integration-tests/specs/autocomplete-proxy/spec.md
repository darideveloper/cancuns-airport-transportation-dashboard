# autocomplete-proxy Spec Delta

## ADDED Requirements

### Requirement: Live API Integration Verification
The system SHALL provide a way to verify the autocomplete proxy against the live legacy API in controlled environments.

#### Scenario: Live Autocomplete Success
- **Given**: The system is configured with valid live credentials.
- **And**: `LIVE_API_TESTS` is enabled.
- **When**: A search request is made to the real legacy API via the proxy.
- **Then**: It MUST return a 200 OK with actual location data.
