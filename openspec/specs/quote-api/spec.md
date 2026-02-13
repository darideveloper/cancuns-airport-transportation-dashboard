# quote-api Specification

## Purpose
TBD - created by archiving change create-quote-proxy-api. Update Purpose after archive.
## Requirements
### Requirement: Proxy Quote Request
> As a public user, I want to get a quote from the legacy system without authentication so that I can see prices. The system MUST proxy the quote request to the legacy API using the stored valid token.

#### Scenario: Success flow
- **Given**: The `QuoteProxyView` endpoint is available publicly.
- **When**: I send a POST request with valid quote parameters (start, end, pax, etc.).
- **Then**: The system internally authenticates with the legacy API.
- **And**: Proxies my request body to the legacy `/quote` endpoint.
- **And**: Returns the legacy API's JSON response to me.

### Requirement: Handle Upstream Errors
> As a system, I want to gracefully handle errors from the legacy API so the frontend receives meaningful statuses. The system SHALL forward upstream error responses to the frontend.

#### Scenario: Pass through error
- **Given**: The legacy API returns a 4xx or 5xx error (e.g., validation error).
- **When**: The `QuoteProxyView` receives this error.
- **Then**: It forwards the status code and error body to the frontend.

