# reservation-proxy

## ADDED Requirements

### Requirement: Send Payment Link for Online Payments
The system SHALL generate a payment link for non-cash reservations (Stripe/PayPal) and return it immediately in the response, suppressing other reservation details.

#### Scenario: Successful Stripe Reservation
- **WHEN** a POST request is sent to `/legacy/create/` with valid details AND `payment_method` set to "STRIPE".
- **THEN** the system SHALL create the reservation via the legacy API.
- **AND** extract the `reservation_id` from the creation response.
- **AND** call the legacy payment link API (`GET /api/v1/reservation/payment/handler`) with `type=STRIPE`.
- **AND** return a JSON response containing ONLY the `payment_link`.

#### Scenario: Successful PayPal Reservation
- **WHEN** a POST request is sent to `/legacy/create/` with valid details AND `payment_method` set to "PAYPAL".
- **THEN** the system SHALL create the reservation via the legacy API.
- **AND** extract the `reservation_id` from the creation response.
- **AND** call the legacy payment link API (`GET /api/v1/reservation/payment/handler`) with `type=PAYPAL`.
- **AND** return a JSON response containing ONLY the `payment_link`.

#### Scenario: Cash Reservation Handling
- **WHEN** `payment_method` is missing, "CASH", or other values not in ["STRIPE", "PAYPAL"].
- **THEN** the system SHALL proceed with standard reservation creation and return the regular reservation details response as per existing spec.

#### Scenario: Payment Link Generation Failure
- **WHEN** the reservation is created successfully but the payment link generation fails (e.g., upstream error).
- **THEN** the system SHALL return a 502 Bad Gateway error indicating failure to generate payment link.
