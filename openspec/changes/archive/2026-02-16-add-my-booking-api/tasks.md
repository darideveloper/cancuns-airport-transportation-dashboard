## 1. Implementation
- [x] 1.1 Add `fetch_my_booking` service function in `legacy_middleware/services.py`
- [x] 1.2 Create `MyBookingProxyView` class in `legacy_middleware/views.py`
- [x] 1.3 Add URL pattern for `/legacy/my-booking/` in `legacy_middleware/urls.py`
- [x] 1.4 Import new view in URLs configuration

## 2. Testing
- [x] 2.1 Create unit tests for `fetch_my_booking` service function
- [x] 2.2 Create integration tests for `MyBookingProxyView`
- [x] 2.3 Test successful booking retrieval scenarios
- [x] 2.4 Test error handling (not found, invalid params, upstream errors)
- [x] 2.5 Test token expiration and retry logic
- [x] 2.6 Test response validation for malformed data

## 3. Edge Cases and Validation
- [x] 3.1 Handle multiple booking identifier types (ID, code, email+phone)
- [x] 3.2 Validate booking identifier format before upstream request
- [x] 3.3 Handle empty or null responses from legacy API
- [x] 3.4 Test with various booking statuses (confirmed, cancelled, pending payment)

## 4. Documentation and Integration
- [x] 4.1 Update API documentation with new endpoint details
- [x] 4.2 Add examples of request/response formats
- [x] 4.3 Verify integration with existing middleware patterns
- [x] 4.4 Run full test suite to ensure no regressions
