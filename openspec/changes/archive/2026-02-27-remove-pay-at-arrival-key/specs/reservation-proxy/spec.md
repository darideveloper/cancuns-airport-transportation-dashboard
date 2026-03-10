# reservation-proxy Specification Delta

## MODIFIED Requirements

### Requirement: Send Payment Link for Online Payments
The system SHALL generate a payment link for non-cash reservations (Stripe/PayPal) and return it immediately in the response, suppressing other reservation details.

#### Scenario: Cash Reservation Handling
- **WHEN** `payment_method` is missing, "CASH", or other values not in ["STRIPE", "PAYPAL"].
- **AND** the system receives any request data.
- **THEN** the system SHALL explicitly strip the `pay_at_arrival` key from the payload before proxying to the legacy API.
- **AND** it SHALL proceed with standard reservation creation and return the regular reservation details response.

#### Scenario: Successful Reservation with Stripped Key
- **WHEN** a POST request is sent to `/legacy/create/` with valid customer details AND a `pay_at_arrival` key.
- **THEN** the system SHALL authenticate with the legacy API if needed.
- **AND** it SHALL strip the `pay_at_arrival` key from the payload.
- **AND** it SHALL inject the `site_id` into the payload.
- **AND** it SHALL return the legacy API's response.
