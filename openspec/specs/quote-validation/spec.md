# quote-validation Specification

## Purpose
TBD - created by archiving change validate-quote-api-response. Update Purpose after archive.
## Requirements
### Requirement: Quote Response Proxying
The middleware MUST validate that the legacy API response is structurally correct before returning it to the frontend.

#### Scenario: Successful Quote with Items
- **GIVEN** a valid request to the Quote endpoint
- **AND** the legacy API returns a `200 OK` with an `items` list and `places` object
- **WHEN** the proxy processes the response
- **THEN** it MUST return `200 OK` with the original data

#### Scenario: No Availability Error
- **GIVEN** a valid request to the Quote endpoint
- **AND** the legacy API returns a `200 OK` with an error object `{"code": "no_availability", ...}`
- **WHEN** the proxy processes the response
- **THEN** it MUST return the error object with its original status code (200) to allow frontend handling

#### Scenario: Upstream Validation Error
- **GIVEN** an invalid request (e.g., missing passengers)
- **AND** the legacy API returns a `422 Unprocessable Entity`
- **WHEN** the proxy processes the response
- **THEN** it MUST return `422 Unprocessable Entity` with the upstream error messages

#### Scenario: Upstream Malformed Response
- **GIVEN** a request to the Quote endpoint
- **AND** the legacy API returns a `200 OK` but without the expected `items` key
- **WHEN** the proxy processes the response
- **THEN** it MUST return `502 Bad Gateway` indicating an upstream data error

