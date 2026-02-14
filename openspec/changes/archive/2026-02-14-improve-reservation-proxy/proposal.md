# Improve Reservation Proxy View

Robustly validate upstream responses and ensure comprehensive test coverage for the `ReservationCreateProxyView`.

## Purpose
The `ReservationCreateProxyView` currently proxies requests to the legacy API and returns the upstream response directly. While effective for simple pass-throughs, it lacks structural validation of the successful response, potentially passing malformed data to the client if the upstream API behaves unexpectedly. Additionally, the critical reservation creation flow currently lacks dedicated test coverage. This proposal addresses these gaps by implementing response validation and a full suite of unit and integration tests.

## Why
- **Reliability**: Ensures the API contract (e.g., presence of `reservation_id`) is upheld even if the upstream API falters.
- **Maintainability**: Prevents silent failures in the frontend by catching malformed responses early at the proxy layer.
- **Confidence**: Comprehensive tests (both mock and live) guarantee the integration works correctly across various scenarios (success, auth retry, validation errors).

## Background
The `ReservationCreateProxyView` was recently introduced to facilitate booking creation via the legacy system. Similar to `QuoteProxyView`, it handles token authentication. However, unlike `QuoteProxyView`, it currently does not validate the structure of the 200 OK response from the legacy system.

Additionally, a critical testing gap exists: the current test suite mocks service functions (e.g., `fetch_quote`, `fetch_reservation_create`) at the view level, which means the logic *inside* these service functions—specifically the injection of default parameters like `site_id` and `rate_group`—is never actually executed or verified. This creates a blind spot where configuration-dependent behavior could silently fail.

## Timing
This improvement should be implemented immediately to ensure the stability of the booking flow before wider rollout.
