# Design: Cloud Storage and Storage-Independent Media Resolution

## Context
The project needs to serve static and media files from S3-compatible cloud providers (AWS, DigitalOcean) in production while defaulting to local storage in development. Furthermore, some legacy or Railway-specific storage links must be handled gracefully by the system's URL resolution utility.

## Goals
- Support `STORAGE_AWS` environment variable to toggle between local and cloud storage.
- Provide folder-based isolation (`AWS_PROJECT_FOLDER`) to allow sharing a single bucket across multiple projects or environments.
- Support `AWS S3`, `DigitalOcean Spaces`, and `Railway Storage` links in `get_media_url`.

## Decisions

### 1. Storage Backends Implementation
- File: `project/storage_backends.py`
- Inherit from `S3Boto3Storage` to define:
  - `StaticStorage`: For collected static files (`location = STATIC_LOCATION`).
  - `PublicMediaStorage`: For user uploads with public access (`location = PUBLIC_MEDIA_LOCATION`).
  - `PrivateMediaStorage`: For restricted files, bypassing CDN for Signed URLs (`custom_domain = False`).

### 2. URL Resolution Strategy
- Update `utils/media.py` to check for specific domain strings:
  - `s3.amazonaws.com`
  - `digitaloceanspaces`
  - `storage.railway.app`
- If any of these strings are present, the URL is assumed to be absolute.
- Otherwise, the URL is prefixed with `settings.HOST`.

### 3. Settings Integration
- Use `STORAGES` dictionary in `settings.py` (Django 4.2+ standard) instead of deprecated `DEFAULT_FILE_STORAGE`.
- Configuration logic:
  ```python
  if STORAGE_AWS:
      STORAGES = {
          "default": {"BACKEND": "project.storage_backends.PublicMediaStorage"},
          "staticfiles": {"BACKEND": "project.storage_backends.StaticStorage"},
          "private": {"BACKEND": "project.storage_backends.PrivateMediaStorage"},
      }
  else:
      STORAGES = { ... local defaults ... }
  ```

## Risks / Trade-offs
- **CDN Invalidation**: Cloud storage often relies on high `Cache-Control` headers (e.g., `max-age=86400`). Immediate updates to static files may require CDN invalidation.
- **Signed URLs**: `PrivateMediaStorage` requires `custom_domain = False` to ensure `boto3` generates valid signed URLs, which may impact performance if the primary bucket is far from the user.
