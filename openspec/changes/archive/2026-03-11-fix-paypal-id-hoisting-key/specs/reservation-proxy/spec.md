# Spec: Reservation Proxy API Updates

## MODIFIED Requirements

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
