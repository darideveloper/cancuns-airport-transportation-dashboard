# Design: Response Validation & Tests

## Validation Logic
The `ReservationCreateProxyView` will implement a `validate_reservation_response` method with enhanced robustness.

```python
    def validate_reservation_response(self, data):
        # 0. Safety check: Ensure data is a dictionary
        if not isinstance(data, dict):
            return Response(
                {"error": "Upstream response malformed: expected JSON object"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        # 1. Pass through if upstream reports an application-level error
        if "error" in data:
            return None

        # 2. Check for success indicators
        # The legacy API typically returns 'reservation_id' or 'id' on success.
        has_id = "reservation_id" in data or "id" in data
        
        if not has_id:
            return Response(
                {"error": "Upstream response malformed: missing reservation ID"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        return None
```

**Rationale for Type Check**: The upstream API could theoretically return a list or primitive value instead of a JSON object. Without the `isinstance(data, dict)` check, the subsequent `"error" in data` and `"reservation_id" in data` checks would raise a `TypeError`.

## Test Architecture
We will create a comprehensive three-layer testing strategy:

### 1. Service Layer Tests (`legacy_middleware/tests/test_services.py`)
**Purpose**: Verify the service functions' logic in isolation by mocking only `requests.post`.

**Coverage**:
- `fetch_reservation_create`:
    - Injects `site_id` from settings when missing in payload.
    - Preserves existing `site_id` if present.
    - Sends correct `Authorization: Bearer <token>` header.
- `fetch_quote` (bonus cleanup):
    - Injects `rate_group` from settings when missing.

**Why**: The current test suite mocks service functions at the view level, meaning the parameter injection logic is never executed. This creates a blind spot.

### 2. View Layer Tests (`legacy_middleware/tests/test_views.py`)
**Purpose**: Verify view-specific logic by mocking the service functions.

**Coverage**:
- Token retrieval and refresh flow.
- Response validation (`validate_reservation_response`).
- Error code mapping (502, 422).
- Malformed response handling (non-dict, missing ID).

**Strategy**: Mock `fetch_reservation_create` to return controlled responses. This isolates the view logic from the service layer.

### 3. Integration Tests (`ReservationCreateProxyLiveTests`)
**Purpose**: Verify end-to-end flow against the real legacy API.

**Strategy**:
1.  Fetch valid location IDs using the autocomplete proxy.
2.  Construct a valid booking payload.
3.  Send the request to the local Django proxy.
4.  Assert that a Reservation ID is returned.

**Note**: These tests create real data in the legacy system and should only run when `LIVE_API_TESTS=True`.

