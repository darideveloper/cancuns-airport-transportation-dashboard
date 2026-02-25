# Tasks: Translate Visible Model and Admin Texts to English

- [x] Update project conventions in `openspec/project.md` <!-- id: 0 -->
- [x] Translate `blog/models.py` <!-- id: 1 -->
    - [x] Translate `Post` field labels and help texts
    - [x] Translate `Post.LANGS` choices
    - [x] Uncomment and translate `Post.Meta`
    - [x] Translate `Image` field labels
    - [x] Uncomment and translate `Image.Meta`
- [x] Translate `blog/admin.py` <!-- id: 2 -->
    - [x] Translate `ImageAdmin.copy_link` description
    - [x] Translate success message in `copy_link`
- [x] Translate `project/admin.py` <!-- id: 3 -->
    - [x] Translate "Editar" to "Edit" in `ModelAdminUnfoldBase.edit`
- [x] Generate and apply Django migrations for the `blog` app <!-- id: 4 -->
- [x] Verify changes manually in Admin UI <!-- id: 5 -->
- [x] Run existing tests to ensure no regressions <!-- id: 6 -->
    - [x] `python manage.py test blog`
