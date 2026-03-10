# Design: Remove 'pay_at_arrival' key from Reservation API

## Summary
The goal is to eliminate the `pay_at_arrival` key from the entire integration chain, from the client's perspective down to the legacy API.

## Implementation Details

### 1. Middleware Strategy
The `ReservationCreateProxyView` in `legacy_middleware/views.py` will be modified to ensure the `pay_at_arrival` key is stripped from `request.data` before passing it to `fetch_reservation_create`. This provides a clean interface that guarantees no `pay_at_arrival` key ever reaches the legacy API from this middleware.

```python
# Pseudo-code
class ReservationCreateProxyView(BaseLegacyProxyView):
    def post(self, request, *args, **kwargs):
        # 1. Strip redundant key
        data = request.data.copy()
        data.pop('pay_at_arrival', None)
        
        # 2. Create Reservation using the cleaned data
        response = self.execute_proxy_request(
            fetch_reservation_create,
            data,
            validate_func=self.validate_reservation_response,
        )
        ...
```

### 2. Test Updates
All test cases in `legacy_middleware/tests/test_views.py` that rely on `pay_at_arrival: 1` will be updated to remove it. Since the view's logic for payment link generation already uses `payment_method`, these tests should still work correctly (either defaulting to cash or explicitly using `payment_method: CASH`).

### 3. Documentation Sanitization
A recursive search and replacement will be performed on all Markdown files in `docs/` to remove any references to `pay_at_arrival`. This includes table entries, JSON examples, and descriptive text.

## Trade-offs
- **Legacy API Defaults:** If the legacy API *requires* `pay_at_arrival` for cash payments and doesn't support `payment_method` for that purpose, this change might break cash reservations. However, the current `ReservationCreateProxyView` already ignores it in its own logic, suggesting it's redundant. If it's truly required by the legacy API, the user wouldn't have asked for it to be "completely removed".
