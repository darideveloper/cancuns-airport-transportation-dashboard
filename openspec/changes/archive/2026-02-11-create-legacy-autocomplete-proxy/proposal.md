# Create Legacy API Autocomplete Proxy

Middleware endpoint to securely proxy autocomplete requests to the legacy Caribbean Transfers API without exposing the secret `app-key` to the frontend.

## Goals

1.  Create a Django endpoint `/api/legacy/autocomplete` (or similar) that acts as a secure proxy.
2.  Hide the `app-key` required by the legacy API from the client-side.
3.  Return the same data format as the original legacy endpoint.
4.  Ensure proper environment variable configuration for the legacy API credentials.

## Context

The current `legacy-api.md` documentation describes an existing Laravel legacy API. We need to integrate this legacy API into our Django application as a middleware layer to support a new SSG frontend. The goal is to avoid exposing sensitive keys in the client-side code. This proposal specifically addresses the **Autocomplete** feature.

## Non-Goals

- Implementation of other legacy endpoints (OAuth, Quote, Reservation, etc.).
- Authentication for THIS endpoint (it is public for the frontend, but the backend handles the legacy auth via `app-key`).
- Frontend implementation (this is backend only).

## Technical Requirements

1.  **Environment Variables**:
    - `LEGACY_API_BASE_URL`: The base URL of the legacy API.
    - `LEGACY_API_KEY`: The `app-key` for the autocomplete endpoint.

2.  **Endpoint**:
    - **URL**: `/api/legacy/autocomplete/` (POST, matching legacy method).
    - **Input**: JSON with `keyword`.
    - **Output**: JSON with `items` list, identical to legacy response.

3.  **Logic**:
    - Receive POST request with `keyword`.
    - Validate `keyword` presence.
    - Make a server-side HTTP request to `${LEGACY_API_BASE_URL}/api/v1/autocomplete-affiliates`.
    - Inject `app-key: ${LEGACY_API_KEY}` header.
    - Return the response directly to the client.

## Testing Strategy

- **Mocking**: All external calls to the legacy API MUST be mocked in tests to avoid network dependencies and quota usage.
- **Scenarios**:
    - **Success**: Valid keyword returns mocked list of places.
    - **Validation Error**: Missing keyword in request returns 400 Bad Request.
    - **Legacy API Error**: 500/502 response from legacy API is handled gracefully (e.g., returned as 502 Bad Gateway or 500 Internal Server Error with details).
