## MODIFIED Requirements
### Requirement: Default Local Storage
The system SHALL use the local filesystem for all file storage when `STORAGE_AWS` is `False`.

#### Scenario: Media File Upload (Local)
- **WHEN** `STORAGE_AWS` is set to `False`
- **AND** a user uploads an image file
- **THEN** the file MUST be saved in the `MEDIA_ROOT` directory on the local disk
- **AND** the file URL MUST start with `MEDIA_URL` (typically `/media/`)

## ADDED Requirements
### Requirement: Cloud Storage Support
The system SHALL support AWS S3 and DigitalOcean Spaces for file storage when `STORAGE_AWS` is `True`.

#### Scenario: Media File Upload (Cloud)
- **WHEN** `STORAGE_AWS` is set to `True`
- **AND** valid AWS/S3 credentials are provided
- **THEN** uploaded files MUST be stored in the configured S3 bucket
- **AND** the file URL MUST point to the cloud provider's domain (AWS or DigitalOcean)

### Requirement: Cross-Platform Media URL Resolution
The `get_media_url` utility SHALL return absolute URLs for files stored in AWS, DigitalOcean, Railway, or the local filesystem.

#### Scenario: Resolve Railway Storage Link
- **WHEN** `get_media_url` is called with a URL containing `storage.railway.app`
- **THEN** it MUST return the URL as is (absolute)

#### Scenario: Resolve DigitalOcean Spaces Link
- **WHEN** `get_media_url` is called with a URL containing `digitaloceanspaces`
- **THEN** it MUST return the URL as is (absolute)

#### Scenario: Resolve Local Link
- **WHEN** `get_media_url` is called with a relative path (e.g., `/media/test.png`)
- **THEN** it MUST prefix the path with the `HOST` setting
