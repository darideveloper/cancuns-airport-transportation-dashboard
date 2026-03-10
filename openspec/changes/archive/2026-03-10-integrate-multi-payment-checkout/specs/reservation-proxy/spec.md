# reservation-proxy Specification Update

## MODIFIED Requirements

### Requirement: Send Payment Link for Online Payments
The system SHALL generate a payment link for non-cash reservations (Stripe/PayPal/Credit Card) and return it along with all payment provider metadata (e.g. `paypal_id`) and reservation metadata (e.g. `uuid`).

#### Scenario: Successful Stripe Reservation
- **WHEN** a POST request is sent to `/legacy/create/` with valid details AND `payment_method` set to "STRIPE".
- **THEN** the system SHALL create the reservation via the legacy API.
- **AND** extract the `reservation_id` from the creation response.
- **AND** call the legacy payment link API (`GET /api/v1/reservation/payment/handler`) with `type=STRIPE`.
- **AND** return a JSON response containing `payment_link`, `reservation_id`, and `uuid` (if available).

#### Scenario: Successful PayPal Reservation
- **WHEN** a POST request is sent to `/legacy/create/` with valid details AND `payment_method` set to "PAYPAL" or "CREDIT_CARD".
- **THEN** the system SHALL map `CREDIT_CARD` to "PAYPAL" if needed.
- **AND** create the reservation via the legacy API.
- **AND** extract the `reservation_id` from the creation response.
- **AND** call the legacy payment link API (`GET /api/v1/reservation/payment/handler`) with `type=PAYPAL`.
- **AND** return a JSON response containing `payment_link`, `reservation_id`, `uuid` (if available), and all fields returned by the legacy payment API (including `paypal_id`).

## ADDED Requirements

### Requirement: PayPal Order Capture Proxy
The system MUST provide an endpoint to capture a PayPal order via the legacy API.

#### Scenario: Successful PayPal Capture
- **WHEN** a POST request is sent to `/legacy/capture/` with a valid PayPal Order `id`.
- **THEN** the system SHALL call the legacy capture API (`GET /api/v1/reservation/payment/paypal/capture-order`).
- **AND** return the upstream capture response to the client.

#### Scenario: Capture Missing Order ID
- **WHEN** a POST request is sent to `/legacy/capture/` without an `id`.
- **THEN** the system SHALL return a 400 Bad Request error.
