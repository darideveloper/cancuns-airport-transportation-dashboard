# reservation-proxy Specification

## Purpose
The system MUST provide a proxy endpoint to create bookings in the legacy system, handling authentication and common parameters automatically.
## Requirements
### Requirement: Create Reservation Proxy
The system SHALL provide a public endpoint that proxies reservation creation requests to the legacy API. It MUST automatically handle JWT authentication and inject the default `site_id`.

#### Scenario: Successful Cash Reservation
- **WHEN** a POST request is sent to `/legacy/create/` with `payment_method` set to "CASH".
- **THEN** the system SHALL inject `"pay_at_arrival": 1` into the payload sent to the legacy API.
- **AND** return a standardized response including `reservation_id`, `uuid`, and `payment_method`.

#### Scenario: Successful Online Reservation (Stripe/PayPal)
- **WHEN** a POST request is sent to `/legacy/create/` with an online `payment_method`.
- **THEN** the system SHALL omit `"pay_at_arrival"` from the legacy API payload.

### Requirement: Response Validation
The system MUST validate the structural integrity of successful upstream responses (200 OK) to prevent passing malformed data to the client.

#### Scenario: Malformed Success Response
- **WHEN** the upstream API returns 200 OK but with missing critical fields (e.g., `reservation_id` or `id`).
- **THEN** the system SHALL return a 502 Bad Gateway error indicating a malformed response.

### Requirement: Send Payment Link for Online Payments
The system SHALL generate a payment link for non-cash reservations (Stripe/PayPal/Credit Card) and return it along with all payment provider metadata (e.g. `paypal_id`) and reservation metadata (e.g. `uuid`).

#### Scenario: Successful PayPal-V2 Reservation
- **WHEN** a POST request is sent to `/legacy/create/` with `payment_method` set to "PAYPAL" or "CREDIT_CARD".
- **THEN** the system SHALL call the legacy payment link API (`GET /api/v1/reservation/payment/handler`) with `type=PAYPAL-V2`.
- **AND** return a standardized JSON response containing `reservation_id`, `uuid`, `payment_method`, and `payment_data`.

#### Scenario: Original Payment Method Preservation
- **WHEN** a POST request is sent with `payment_method` as "CREDIT_CARD".
- **THEN** the system SHALL map it to "PAYPAL-V2" internally for the upstream call.
- **AND** return `"payment_method": "CREDIT_CARD"` in the response.

### Requirement: PayPal Order Capture Proxy
The system MUST provide an endpoint to capture a PayPal order via the legacy API.

#### Scenario: Successful PayPal Capture
- **WHEN** a POST request is sent to `/legacy/capture/` with a valid PayPal Order `id`.
- **THEN** the system SHALL call the legacy capture API (`GET /api/v1/reservation/payment/paypal/capture-order`).
- **AND** return the upstream capture response to the client.

#### Scenario: Capture Missing Order ID
- **WHEN** a POST request is sent to `/legacy/capture/` without an `id`.
- **THEN** the system SHALL return a 400 Bad Request error.

### Requirement: Standardized Proxy Response
The response from the reservation creation proxy MUST correctly identify the PayPal Order ID and hoist it to the top level.

#### Scenario: PayPal-V2 Order ID Hoisting
- **Given** a successful reservation creation with `PAYPAL` or `CREDIT_CARD` method
- **When** the proxy receives a response from the `PAYPAL-V2` provider containing an ID in the `url` field
- **Then** the proxy MUST include that ID as `paypal_id` at the top level of the JSON response payload.

#### Scenario: Explicit PayPal ID Hoisting
- **Given** a successful reservation creation with an online payment method
- **When** the proxy receives a response containing an explicit `paypal_id` field in `payment_data`
- **Then** that value MUST be hoisted to the top level of the JSON response payload as `paypal_id`.

### Requirement: Field Mapping for Legacy Compatibility
The proxy SHALL ensure that data received from the frontend is correctly mapped to the fields expected by the legacy API.

#### Scenario: Request Field Translation
- **Given** a reservation creation request from the frontend
- **When** the proxy forwards the payload to the legacy system
- **Then** it MUST perform the following field mappings:
  - `flightNumber` -> `flight_number`
  - `notes` -> `comments`
  - `firstName` -> `first_name`
  - `lastName` -> `last_name`
  - `email` -> `email_address`

