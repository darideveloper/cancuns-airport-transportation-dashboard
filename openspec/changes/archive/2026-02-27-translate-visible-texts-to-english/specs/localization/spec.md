# Specification: Localization and Model Translation

## ADDED Requirements

### Requirement: English standard for metadata
The project MUST use English for all `verbose_name`, `help_text`, and `choices` labels in Django models and admin classes.

#### Scenario: Metadata definition
- **Given** a new model or field is added
- **When** defining its `verbose_name` or `help_text`
- **Then** the string MUST be in English.

### Requirement: Blog model translations
The `blog` app models MUST be fully translated to English.

#### Scenario: Post model labels
- **Given** the `Post` model in `blog/models.py`
- **When** viewed in the Admin interface
- **Then** all field labels (Title, Language, Banner URL, etc.) MUST be in English.
- **And** the model names (Post, Posts) MUST be in English.

#### Scenario: Image model labels
- **Given** the `Image` model in `blog/models.py`
- **When** viewed in the Admin interface
- **Then** all field labels (Name, Image, etc.) MUST be in English.
- **And** the model names (Image, Images) MUST be in English.

### Requirement: Base Admin translations
Common admin actions defined in the base classes MUST be in English.

#### Scenario: Edit action
- **Given** the `ModelAdminUnfoldBase` in `project/admin.py`
- **When** the "Edit" action is displayed in any model list
- **Then** its label MUST be "Edit".
