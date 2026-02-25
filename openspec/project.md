# Project Context

## Purpose
Cancun Airport Transportation (CAT) Dashboard is a backend administrative system designed to manage transportation services, blog content, and operational data for an airport shuttle provider in Cancun. Its primary goals are to provide a premium management interface for staff and a robust API for the related landing pages.

## Tech Stack
- **Backend Framework**: Python 3.x with Django 5.2
- **API Framework**: Django Rest Framework (DRF)
- **Admin Interface**: Django Unfold (Customized with OKLCH color palettes)
- **Database**: PostgreSQL (Production), SQLite (Testing/Development)
- **File Storage**: AWS S3 (via django-storages and boto3) or Local FileSystem
- **Static Assets**: WhiteNoise for optimized serving
- **Styling**: Tailwind CSS (integrated into Admin via custom scripts) and Vanilla CSS
- **Testing**: Selenium and Django's native TestCase

## Project Conventions

### Code Style
- **Naming Conventions**: 
    - Models: `PascalCase`
    - Fields/Variables: `snake_case`
    - Admin Classes: `[ModelName]Admin`
- **Formatting**: PEP 8 for Python. Use `clsx` for conditional classes in any frontend components (React/Astro).
- **Localization**: Projects use English as the default language for metadata. All `verbose_name` and `help_text` in models should be in English.

### Architecture Patterns
- **Base Admin**: Centralized logic in `project/admin.py` via `ModelAdminUnfoldBase` to ensure consistent UI (compressed fields, unsaved form warnings, global date filters).
- **Custom Widgets**: `TextField` attributes in Admin are automatically overridden with `WysiwygWidget`.
- **Slugs**: Auto-generated in model `save()` methods using `slugify(title)` if not provided.
- **API Response**: Custom pagination (`CustomPageNumberPagination`) and custom exception handlers are used globally.

### Testing Strategy
- **Unit/Integration Tests**: Standard Django tests using SQLite.
- **End-to-End**: Selenium for browser-based testing.
- **Environment**: Configurable via `TEST_HEADLESS` environment variable for CI/CD compatibility.

### Git Workflow
- Standard feature-branch workflow.
- Commits should be descriptive and relate to specific features or fixes.

## Domain Context
- **Industry**: Travel and Transportation (Airport Transfers).
- **Location Focus**: Cancun/Riviera Maya region.
- **Core Entities**: Posts (Blog), Images, Users, and Leads (implied).
- **Language**: Operations are primarily in Spanish but support English content (e.g., Blog translations).

## Important Constraints
- **Performance**: Static files must be served efficiently via WhiteNoise or S3.
- **UI/UX**: The Admin dashboard must maintain a premium "Orange Accent" theme as defined in `UNFOLD` settings.
- **Authentication**: APIs strictly require Token or Session authentication.

## External Dependencies
- **Tawk.to**: Customer chat widget integration.
- **AWS S3**: Primary storage for media and static assets in production.
- **SMTP**: For lead notifications and system emails.
