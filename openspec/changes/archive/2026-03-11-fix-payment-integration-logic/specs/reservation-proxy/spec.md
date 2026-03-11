# reservation-proxy Specification Update

## MODIFIED Requirements

### Requirement: Create Reservation Proxy
The system SHALL provide a public endpoint that proxies reservation creation requests to the legacy API. It MUST automatically handle JWT authentication and inject the default `site_id`.

#### Scenario: Successful Cash Reservation
- **WHEN** a POST request is sent to `/legacy/create/` with `payment_method` set to "CASH".
- **THEN** the system SHALL inject `"pay_at_arrival": 1` into the payload sent to the legacy API.
- **AND** return a standardized response including `reservation_id`, `uuid`, and `payment_method`.

#### Scenario: Successful Online Reservation (Stripe/PayPal)
- **WHEN** a POST request is sent to `/legacy/create/` with an online `payment_method`.
- **THEN** the system SHALL omit `"pay_at_arrival"` from the legacy API payload.

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

## ADDED Requirements

### Requirement: Standardized Proxy Response
The system MUST provide a consistent JSON response structure for all successful reservation creation requests.

#### Scenario: Standardized Response Success
- **WHEN** a reservation is successfully created (any method).
- **THEN** the response MUST include:
  - `reservation_id`: (int/str) The legacy ID.
  - `uuid`: (str) The reservation UUID.
  - `payment_method`: (str) The original requested method.
  - `payment_data`: (dict) Provider metadata (empty for CASH).
