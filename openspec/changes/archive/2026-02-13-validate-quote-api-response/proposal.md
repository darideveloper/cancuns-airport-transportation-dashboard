# Proposal: Validate Quote API Response

This proposal covers the enhancement of the Quote API proxy to include stricter validation of the upstream response and more comprehensive testing of various edge cases, including "No Availability" and malformed data scenarios.

## Problem Statement

The current `QuoteProxyView` implementation is a thin wrapper that passes through the upstream legacy API response regardless of its structure (as long as it's valid JSON). While functional, it lacks:

1.  **Differentiated Handling of "No Availability"**: The legacy API returns a `200 OK` even when no services are available, using an error object in the body. The middleware should ideally detect this to ensure the frontend receives consistent error reporting.
2.  **Schema Validation**: If the upstream API returns a `200 OK` but misses critical fields like `items` or `places`, the middleware currently passes this partial data to the client.
3.  **Comprehensive Coverage**: Tests do not currently cover the "No Availability" scenario or the specific structure of returned items.

## Proposed Changes

### Middleware (`views.py`)
- Enhance `QuoteProxyView` to inspect the response body when status is `200 OK`.
- If an `error` object with `code: "no_availability"` is present, ensure it's handled as a known application error.
- Validate that a successful response contains an `items` list and `places` object.

### Testing (`tests/test_views.py`)
- Enhance existing tests and add new cases for:
    - Success with realistic payload (must contain `items` and `places`).
    - "No Availability" error returned as 200 (upstream behavior) - ensure it passes through.
    - Validation error (422) handling (verify pass-through).
    - Malformed JSON handling (returns 502).
    - Missing `items` or `places` key in 200 OK response (returns 502).

## Expected Outcome
- Improved reliability of the Quote API proxy.
- Guaranteed structure for the frontend, making it easier to implement robust UI handling.
- Better documentation through tests of how the legacy API behaves in edge cases.
