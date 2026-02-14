# Proposal: Refactor Legacy Middleware for DRY

## Problem
The `legacy_middleware` module currently contains significant code duplication across its views and services. Specifically:
- `QuoteProxyView` and `ReservationCreateProxyView` have identical logic for token retrieval, refresh, and retry (401 handling).
- Error handling for upstream `requests` and JSON parsing is repeated.
- `services.py` has multiple functions that build similar POST requests with minor variations in payload injection.

## Solution
Apply the DRY (Don't Repeat Yourself) principle by:
1.  **Extracting Authentication Logic**: Create a base class or mixin for `APIView` that handles common token operations (get valid token, refresh on 401, retry).
2.  **Centralizing Error Handling**: Move upstream error mapping (e.g., mapping `RequestException` to `502 Bad Gateway`) into a common utility or base class method.
3.  **Refactoring services.py**: Implement a generic internal helper for making POST requests to the legacy API, reducing repetition in `fetch_quote`, `fetch_reservation_create`, etc.

## Impact
- **Maintainability**: Changes to the legacy API's auth or error patterns only need to be updated in one place.
- **Readability**: Smaller, more focused views and services.
- **Robustness**: Consistent error handling across all proxy endpoints.
