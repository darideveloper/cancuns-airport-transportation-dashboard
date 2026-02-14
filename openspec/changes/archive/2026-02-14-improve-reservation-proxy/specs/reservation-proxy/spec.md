# reservation-proxy Specification

## ADDED Requirements

### Requirement: Response Validation
The system MUST validate the structural integrity of successful upstream responses (200 OK) to prevent passing malformed data to the client.

#### Scenario: Malformed Success Response
- **WHEN** the upstream API returns 200 OK but with missing critical fields (e.g., `reservation_id` or `id`).
- **THEN** the system SHALL return a 502 Bad Gateway error indicating a malformed response.
