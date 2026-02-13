# Proposal: Add Legacy API Integration Tests

## Summary
Add a suite of integration tests that perform real HTTP requests to the legacy API. These tests will compliment existing unit tests (which use mocks) by verifying that the integration with the live service is functional and that the third-party API behavior matches our assumptions.

## Problem Statement
While unit tests with mocks ensure our code handles theoretical responses correctly, they don't catch:
- Changes in the third-party API structure (API drift).
- Authentication failures with real credentials.
- Connectivity issues or environment-specific configuration errors.

## Proposed Solution
- Implement a new set of tests in `legacy_middleware/tests/test_views.py` that do NOT mock the `requests` library or internal services.
- Use a `tag` (e.g., `integration`) or an environment variable (e.g., `LIVE_API_TESTS`) to skip these tests by default.
- Test the key flows: Autocomplete proxy and Quote proxy.
- Ensure these tests run only when valid credentials are provided in the environment.

## Impact
- **Security**: Verifies that real tokens are handled correctly.
- **Reliability**: Provides early warning of third-party API changes.
- **Performance**: Integration tests are slower than unit tests, hence the need to run them selectively.
