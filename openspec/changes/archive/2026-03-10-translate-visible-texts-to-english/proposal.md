# Proposal: Translate Visible Model and Admin Texts to English

## Problem
The project currently has several visible texts (verbose names, help texts, choice labels, and admin actions) in Spanish, particularly in the `blog` app and the base admin components. The project's current localization convention also mandates Spanish for these fields, which contradicts the new requirement to have everything in English.

## Proposed Solution
1.  Translate all Spanish strings in `blog/models.py`, `blog/admin.py`, and `project/admin.py` to English.
2.  Uncomment and translate the `Meta` class `verbose_name` and `verbose_name_plural` in `blog/models.py`.
3.  Update the project's localization convention in `openspec/project.md` to reflect that English is now the standard for model and admin texts.

## Impact
- **UI**: The Django Admin interface will now be entirely in English for the affected models.
- **Conventions**: Updates the architectural mandates for future development.
- **Tests**: No impact expected on functional tests as these are mostly metadata changes, but Selenium tests that search for Spanish strings might need adjustment (checked: they seem to use IDs or English selectors for preview labels, but I will verify).

## Spec Deltas
- `openspec/changes/translate-visible-texts-to-english/specs/localization/spec.md`: New requirements for project-wide localization standards and specific model translations.
