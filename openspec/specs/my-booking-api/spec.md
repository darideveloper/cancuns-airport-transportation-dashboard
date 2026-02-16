# my-booking-api Specification

## Purpose
TBD - created by archiving change add-my-booking-api. Update Purpose after archive.
## Requirements
### Requirement: Retrieve My Booking Proxy
The system SHALL provide a public endpoint that proxies booking retrieval requests to the legacy API. It MUST automatically handle JWT authentication and validate booking identifiers.

#### Scenario: Successful Booking Retrieval
- **WHEN** a GET request is sent to `/legacy/my-booking/` with valid booking identifier parameters.
- **THEN** the system authenticates with the legacy API if needed.
- **AND** it validates the booking identifier format.
- **AND** it returns the legacy API's 200 OK response with complete booking details.

#### Scenario: Booking Not Found
- **WHEN** the legacy API returns a 404 status code for the booking identifier.
- **THEN** the system SHALL forward the 404 status and error message to the client.

#### Scenario: Invalid Booking Identifier
- **WHEN** a GET request is sent with missing or malformed booking identifier parameters.
- **THEN** the system SHALL return a 400 Bad Request with descriptive error message.

#### Scenario: Token Expiration and Retry
- **WHEN** the legacy API returns a 401 Unauthorized because the cached token expired.
- **THEN** the system SHALL fetch a new token and retry the request once.

#### Scenario: Upstream Unavailable
- **WHEN** the legacy API is unreachable or returns a 5xx error.
- **THEN** the system SHALL return a 502 Bad Gateway with a descriptive error message.

### Requirement: Response Validation
The system MUST validate the structural integrity of successful upstream responses (200 OK) to prevent passing malformed booking data to the client.

#### Scenario: Malformed Success Response
- **WHEN** the upstream API returns 200 OK but with missing critical booking fields (e.g., `reservation_id`, `id`, or `booking_reference`).
- **THEN** the system SHALL return a 502 Bad Gateway error indicating a malformed response.

### Requirement: Support Multiple Booking Identifier Types
The system SHALL support various booking identifier formats used by the legacy system (reservation ID, booking code, confirmation number, etc.).

#### Scenario: Reservation ID Lookup
- **WHEN** a GET request includes `reservation_id` parameter.
- **THEN** the system SHALL use this identifier to query the legacy API.

#### Scenario: Booking Code Lookup
- **WHEN** a GET request includes `booking_code` parameter.
- **THEN** the system SHALL use this identifier to query the legacy API.

#### Scenario: Email and Phone Lookup
- **WHEN** a GET request includes `email` and `phone` parameters for customer verification.
- **THEN** the system SHALL use these credentials to retrieve associated bookings.

### Requirement: Booking Status Information
The system MUST provide comprehensive booking status information including payment status, pickup details, and service type.

#### Scenario: Complete Booking Details
- **WHEN** a booking is successfully retrieved.
- **THEN** the response SHALL include customer details, service information, pickup/dropoff locations, payment status, and booking timestamps.

#### Scenario: Payment Status Integration
- **WHEN** a booking has online payment (Stripe/PayPal).
- **THEN** the response SHALL include current payment status and any pending payment links.

