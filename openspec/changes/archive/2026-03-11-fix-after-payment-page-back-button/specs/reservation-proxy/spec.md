# Spec: Reservation Proxy API Updates

## MODIFIED Requirements

### Requirement: Standardized Proxy Response
The response from the reservation creation proxy MUST be consistent and provide easily accessible data for the frontend.

#### Scenario: Online Payment Response
- **Given** a successful reservation creation with an online payment method (e.g., `PAYPAL`, `STRIPE`)
- **When** the proxy receives the response from the legacy system
- **Then** the response MUST include `reservation_id`, `uuid`, `payment_method`, and `payment_data`
- **And** if a `paypal_id` is returned within `payment_data`, it MUST be hoisted to the top level of the response payload.

#### Scenario: Absolute Redirect URLs
- **Given** the frontend provides `success_url` and `cancel_url`
- **When** the proxy generates a payment link via the legacy system
- **Then** the URLs MUST be passed as absolute URLs as received from the request, without any domain stripping.

## ADDED Requirements

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
