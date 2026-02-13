# quote-api Spec Delta

## ADDED Requirements

### Requirement: Live Quote Integration Verification
The system SHALL provide a way to verify the quote proxy and token management against the live legacy API in controlled environments.

#### Scenario: Live Quote Selection
- **Given**: The system is configured with valid live credentials.
- **And**: `LIVE_API_TESTS` is enabled.
- **When**: A quote request is made through the proxy.
- **Then**: It MUST successfully acquire a real token if needed.
- **And**: It MUST return a 200 OK with actual pricing data from the provider.
