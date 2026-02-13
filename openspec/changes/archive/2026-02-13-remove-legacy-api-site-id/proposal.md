<!-- OPENSPEC:START -->
# Change Proposal: Clean Legacy API Site ID

## Summary
Remove the environment variable `LEGACY_API_SITE_ID` and all its references from the codebase, configuration, and documentation, as it is no longer required for the current operation of the system.

## Motivation
The `LEGACY_API_SITE_ID` variable is deprecated and no longer utilized by the application logic or upstream services. Removing it reduces configuration bloat and prevents confusion for future maintainers.

## Proposed Changes
### Configuration Cleanup
- **Project Settings**: Remove the `LEGACY_API_SITE_ID` assignment in `project/settings.py`.
- **Environment Templates**: Remove `LEGACY_API_SITE_ID` from `.env.example`.
- **Environment Instances**: Remove `LEGACY_API_SITE_ID` from `.env.dev`, `.env.prod-coolify`, and `.env.prod-reailway`.

### Codebase Auditing
- Verify that no remaining logic in `legacy_middleware` or `project` attempts to access `settings.LEGACY_API_SITE_ID`.
<!-- OPENSPEC:END -->
