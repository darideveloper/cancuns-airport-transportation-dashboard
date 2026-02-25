# Tasks: Translate Visible Model and Admin Texts to English

- [ ] Update project conventions in `openspec/project.md` <!-- id: 0 -->
- [ ] Translate `blog/models.py` <!-- id: 1 -->
    - [ ] Translate `Post` field labels and help texts
    - [ ] Translate `Post.LANGS` choices
    - [ ] Uncomment and translate `Post.Meta`
    - [ ] Translate `Image` field labels
    - [ ] Uncomment and translate `Image.Meta`
- [ ] Translate `blog/admin.py` <!-- id: 2 -->
    - [ ] Translate `ImageAdmin.copy_link` description
    - [ ] Translate success message in `copy_link`
- [ ] Translate `project/admin.py` <!-- id: 3 -->
    - [ ] Translate "Editar" to "Edit" in `ModelAdminUnfoldBase.edit`
- [ ] Generate and apply Django migrations for the `blog` app <!-- id: 4 -->
- [ ] Verify changes manually in Admin UI <!-- id: 5 -->
- [ ] Run existing tests to ensure no regressions <!-- id: 6 -->
    - [ ] `python manage.py test blog`
