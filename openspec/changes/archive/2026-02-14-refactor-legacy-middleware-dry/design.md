# Design: Refactor Legacy Middleware for DRY

## Architectural Reasoning

### 1. View Refactoring
The current proxy views (`QuoteProxyView`, `ReservationCreateProxyView`) handle both the business logic (calling specific legacy endpoints) and the infrastructure logic (authentication, retries, error mapping). 

We will introduce a `BaseLegacyProxyView(APIView)` that provides:
- `get_legacy_token()`: Encapsulates `LegacyAPIToken.get_valid_token()` and the `fetch_legacy_token()` fallback.
- `execute_proxy_request(request_func, *args, **kwargs)`: A wrapper that handles the 401 retry logic, JSON parsing, and standard error mapping.

### 2. Service Refactoring
`services.py` contains `fetch_quote` and `fetch_reservation_create` which both:
1.  Construct a URL.
2.  Set headers (including `Authorization`).
3.  Optionally inject default values (`rate_group` or `site_id`).
4.  Perform a `requests.post`.

We will introduce `_post_to_legacy(endpoint, token, payload, timeout=10)` as a private helper. Specific services will use this helper after preparing their specific payload injections.

### 3. Error Mapping
We will standardize the mapping of `requests` exceptions and HTTP error codes to DRF responses:
- `requests.RequestException` -> `502 Bad Gateway` ("Upstream service unreachable")
- `401 Unauthorized` -> Handled by retry logic in view.
- `422 Unprocessable Entity` -> Pass through with original body.
- `Other 4xx` -> Pass through content or generic "Upstream client error".
- `5xx` -> `502 Bad Gateway` ("Upstream service unavailable").

## Trade-offs
- **Abstraction overhead**: Introducing a base class adds a layer of abstraction, which might slightly increase cognitive load for new developers, but the reduction in boilerplate and duplication outweighs this.
- **Specific vs. Generic**: We keep the specific payload injection logic in the individual service functions to maintain clarity on what each endpoint requires.
