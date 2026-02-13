# Tasks: Add Legacy API Integration Tests

- [x] Add `AutocompleteProxyLiveTests` class to `legacy_middleware/tests/test_views.py` <!-- id: 0 -->
    - Use `@tag('integration')`
    - Implement `test_autocomplete_live_success`
- [x] Add `QuoteProxyLiveTests` class to `legacy_middleware/tests/test_views.py` <!-- id: 1 -->
    - Use `@tag('integration')`
    - Implement `test_quote_live_success`
- [x] Add environment variable check to skip integration tests by default <!-- id: 2 -->
    - Use `unittest.skipUnless(os.environ.get('LIVE_API_TESTS') == 'True', ...)`
- [x] Verify live tests manually <!-- id: 3 -->
    - Run `LIVE_API_TESTS=True venv/bin/python manage.py test legacy_middleware/tests/test_views.py --tag=integration`
- [x] Update `autocomplete-proxy` spec with live testing requirement <!-- id: 4 -->
- [x] Update `quote-api` spec with live testing requirement <!-- id: 5 -->
