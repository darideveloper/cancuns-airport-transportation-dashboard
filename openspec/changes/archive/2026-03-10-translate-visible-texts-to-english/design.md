# Design: Translate Visible Model and Admin Texts to English

## Architecture
The translation involves updating static strings within Django Model and Admin classes. Since the project uses Django Unfold, these strings are directly consumed by the UI components.

### 1. Model Updates (`blog/models.py`)
- **Post Model**:
    - `LANGS` dictionary: Convert "Español" to "Spanish" and "Inglés" to "English".
    - `verbose_name` attributes: Translate "Título", "Idioma", "Banner URL", "Descripción corta", "Palabras clave", "Autor", "Entrada relacionada", "Contenido", "Fecha de creación", "Fecha de actualización".
    - `help_text` attributes: Translate "URL de la imagen del banner", "Separadas por comas".
    - `Meta` class: Uncomment and set `verbose_name="Post"` and `verbose_name_plural="Posts"`.
- **Image Model**:
    - `verbose_name` attributes: Translate "Nombre", "Imagen", "Fecha de creación", "Fecha de actualización".
    - `Meta` class: Uncomment and set `verbose_name="Image"` and `verbose_name_plural="Images"`.

### 2. Admin Updates
- **Blog Admin (`blog/admin.py`)**:
    - `ImageAdmin.copy_link` action: Translate description "Copiar link" to "Copy link".
    - `messages.success`: Translate "Copiado al portapapeles" to "Copied to clipboard".
- **Base Admin (`project/admin.py`)**:
    - `ModelAdminUnfoldBase.edit` action: Translate description "Editar" to "Edit".

### 3. Project Documentation (`openspec/project.md`)
- Update the `Localization` section under `Project Conventions` to specify English as the standard language for `verbose_name` and `help_text`.

## Trade-offs
- **Translation Fidelity**: Standard technical terms (e.g., "Slug") remain unchanged.
- **Migration Impact**: Since these changes only affect `verbose_name` and `help_text`, they will generate new migrations. While these don't affect the database schema structure, they ensure the metadata is consistent across environments.

## Verification Plan
- **Manual Verification**: Launch the Django Admin and verify that all labels for `Post` and `Image` models are in English.
- **Automated Tests**: Run existing tests in `blog/tests/` to ensure no regression in logic.
