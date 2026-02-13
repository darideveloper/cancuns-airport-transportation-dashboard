# Refactor LegacyAPIToken to Singleton

## Why
The `LegacyAPIToken` model currently allows multiple rows, but the application only needs one valid token at a time. Using a Singleton pattern enforces this constraint at the model level, simplifies retrieval logic, and prevents database clutter.

## What Changes
1.  **Dependency**: Add `django-solo` to the project for Singleton support.
2.  **Model**: Refactor `LegacyAPIToken` to inherit from `SingletonModel`.
3.  **Admin**: Update `LegacyAPITokenAdmin` to use `SingletonModelAdmin`.
4.  **Logic**: Update `get_valid_token` and `QuoteProxyView` to update the single instance instead of creating new rows.
5.  **Testing**: Create `legacy_middleware/tests/test_models.py` to verify singleton behavior.

## Design
-   **Model**: `LegacyAPIToken(SingletonModel)`.
-   **Service**:
    -   `get_valid_token` will retrieve the singleton instance.
    -   If the token is expired or missing, the view will fetch a new one and update the attributes of the singleton instance rather than creating a new record.

## Implementation Plan
1.  Add `django-solo` to `requirements.txt`.
2.  Add `solo` to `INSTALLED_APPS` in `project/settings.py`.
3.  Update `legacy_middleware/models.py`.
4.  Update `legacy_middleware/admin.py`.
5.  Update `legacy_middleware/views.py`.
6.  Create `legacy_middleware/tests/test_models.py` and run tests.
