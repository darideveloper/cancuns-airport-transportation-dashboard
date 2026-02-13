# Design: Legacy API Integration Tests

## Architecture Overview
The integration tests will coexist with unit tests in `legacy_middleware/tests/test_views.py` but will be separated by class and execution logic.

## Technical Details

### Test Separation
We will use Django's `@tag` decorator and `unittest.skipUnless` to manage test execution.

```python
from django.test import tag
import os

@tag('integration')
@unittest.skipUnless(os.environ.get('LIVE_API_TESTS') == 'True', 'Integration tests skipped')
class AutocompleteProxyLiveTests(TestCase):
    # ...
```

### Authentication Handling
For the `QuoteProxyLiveTests`, the tests will hit the real `fetch_legacy_token` service, which will call the live OAuth endpoint. This requires `LEGACY_API_KEY` and other sensitive environment variables to be correctly set in the local `.env.dev` or environment.

### Coverage
1. **Autocomplete Live**: Verifies that a search for a common keyword (e.g., "Cancun") returns valid JSON results from the provider.
2. **Quote Live**: Verifies that requesting a quote for a common route (with real token acquisition) results in a valid price list.

## Trade-offs
- **Dependencies**: These tests require an internet connection and valid API credentials.
- **Maintenance**: If the legacy API goes down for maintenance, these tests will fail. 
- **Cost/Limits**: We must ensure these tests don't consume excessive quota on the provider's side.
