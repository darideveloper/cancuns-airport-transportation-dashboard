<!-- OPENSPEC:START -->
# Spec: Cleanup Legacy API Site ID

## REMOVED Requirements

### Requirement: Remove `LEGACY_API_SITE_ID` from Project

The application MUST NOT require or use the `LEGACY_API_SITE_ID` environment variable.

#### Scenario: Verify Codebase Cleanup
- **Given** the repository is checked for `LEGACY_API_SITE_ID` string,
- **When** the search is performed (excluding archived specs and logs),
- **Then** no matches should be found in active code or configuration files.

#### Scenario: Verify Settings Cleanup
- **Given** `project/settings.py` is inspected,
- **When** checking for `LEGACY_API_SITE_ID`,
- **Then** the variable definition should not be present.

#### Scenario: Verify Env Files Cleanup
- **Given** environment files (`.env.dev`, `.env.example`, etc.),
- **When** checking for `LEGACY_API_SITE_ID`,
- **Then** the key should not be present.
<!-- OPENSPEC:END -->
