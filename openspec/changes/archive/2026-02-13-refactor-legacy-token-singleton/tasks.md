# Tasks

- [x] Add `django-solo` to `requirements.txt` <!-- id: 0 -->
- [x] Add `solo` to `INSTALLED_APPS` in `project/settings.py` <!-- id: 1 -->
- [x] Update `LegacyAPIToken` model to inherit from `SingletonModel` <!-- id: 2 -->
- [x] Update `LegacyAPITokenAdmin` to inherit from `SingletonModelAdmin` <!-- id: 3 -->
- [x] Update `LegacyAPIToken.get_valid_token` logic <!-- id: 4 -->
- [x] Update `QuoteProxyView` to use singleton instance logic <!-- id: 5 -->
- [x] Run migrations <!-- id: 6 -->
- [x] Create `legacy_middleware/tests/test_models.py` with singleton tests <!-- id: 8 -->
- [x] Run tests and verify functionality <!-- id: 7 -->
