# reservation-proxy Specification

## Purpose
The system MUST provide a proxy endpoint to create bookings in the legacy system, handling authentication and common parameters automatically.
## Requirements
### Requirement: Create Reservation Proxy
The system SHALL provide a public endpoint that proxies reservation creation requests to the legacy API. It MUST automatically handle JWT authentication and inject the default `site_id`.

#### Scenario: Successful Reservation
- **WHEN** a POST request is sent to `/legacy/create/` with valid customer details and a service token.
- **THEN** the system authenticates with the legacy API if needed.
- **AND** it injects the `site_id` into the payload.
- **AND** it returns the legacy API's 200 OK response with booking details.

#### Scenario: Validation Error from Upstream
- **WHEN** the legacy API returns a 422 status code due to invalid data.
- **THEN** the system SHALL forward the 422 status and error message to the client.

#### Scenario: Token Expiration and Retry
- **WHEN** the legacy API returns a 401 Unauthorized because the cached token expired.
- **THEN** the system SHALL fetch a new token and retry the request once.

#### Scenario: Upstream Unavailable
- **WHEN** the legacy API is unreachable or returns a 5xx error.
- **THEN** the system SHALL return a 502 Bad Gateway with a descriptive error message.

### Requirement: Response Validation
The system MUST validate the structural integrity of successful upstream responses (200 OK) to prevent passing malformed data to the client.

#### Scenario: Malformed Success Response
- **WHEN** the upstream API returns 200 OK but with missing critical fields (e.g., `reservation_id` or `id`).
- **THEN** the system SHALL return a 502 Bad Gateway error indicating a malformed response.

