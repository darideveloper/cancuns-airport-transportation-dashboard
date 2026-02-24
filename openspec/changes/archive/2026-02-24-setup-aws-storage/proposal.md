# Change: Setup AWS and DigitalOcean Storage

## Why
To enable scalable cloud storage for media and static files in production environments, as documented in `docs/media-file-storage.md`. This allows the project to use S3-compatible APIs (AWS S3, DigitalOcean Spaces) while maintaining a local fallback for development.

## What Changes
- **Dependencies**: Added `django-storages` and `boto3` to `requirements.txt`.
- **Storage Backends**: Created `project/storage_backends.py` with custom classes for Static, Public Media, and Private Media.
- **Settings**: Updated `project/settings.py` with a `STORAGE_AWS` toggle and necessary cloud credentials/configurations.
- **Utilities**: Updated `utils/media.py` to correctly resolve absolute URLs for AWS, DigitalOcean, and Railway storage links.
- **Specifications**: Updated `storage` capability to include cloud storage requirements.

## Impact
- Affected specs: `storage`
- Affected code: `requirements.txt`, `project/settings.py`, `utils/media.py`
- New files: `project/storage_backends.py`
