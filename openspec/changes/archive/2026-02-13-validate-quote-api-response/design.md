# Design: Quote API Deep Dive

## Research Findings (Legacy API Analysis)

Based on `docs/legacy-api.md`, the Quote API lifecycle is as follows:

### Request Structure
The proxy must pass a JSON payload with:
- `type`: "one-way" | "round-trip"
- `language`: "en" | "es"
- `passengers`: 1-35 (integer)
- `currency`: "USD" | "MXN"
- `rate_group`: "xLjDl18" (Injected by middleware if missing)
- `start`: Location object with `pickup` datetime.
- `end`: Location object (with `pickup` only if round-trip).

### Response Scenarios

#### 1. Success (200 OK)
Returns available vehicles.
```json
{
    "items": [
        {
            "id": 1,
            "name": "Private Standard",
            "price": 89.0,
            "token": "...",
            ...
        }
    ],
    "places": { ... }
}
```
**Constraint**: The `token` in each item is vital for the next step (Create Reservation).

#### 2. No Availability (200 OK)
The API does **not** return a 404 or 204. It returns 200 with an error object.
```json
{
    "error": {
        "code": "no_availability",
        "message": ["No services available for this route"]
    }
}
```

#### 3. Validation Error (422 Unprocessable Entity)
Returned for invalid input (e.g., missing passengers, invalid date).
```json
{
    "error": {
        "code": "validation_error",
        "message": [...]
    }
}
```

#### 4. Authentication Error (401 Unauthorized)
Handled by the middleware's retry logic.

## Logic Refinement

To ensure the final data is valid, the view should perform basic structural checks:
1. If status is `200`:
   - Check if `error` exists. If so, PASS THROUGH the response (or handle specific error codes). DO NOT validate `items` or `places` in this case.
   - If no error, verify `items` exists as a list AND `places` object exists.
   - If `items`/`places` are missing or malformed, return `502 Bad Gateway` (Upstream malformed).

## Test Data Strategy
Tests should use realistic mock data inspired by the documentation to ensure the proxy doesn't just pass "any" JSON, but "valid" JSON for our application's needs.
