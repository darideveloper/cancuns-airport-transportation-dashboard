from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin


from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from unfold.decorators import action
from unfold.paginator import InfinitePaginator


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


class ModelAdminUnfoldBase(ModelAdmin):
    # UI setup
    compressed_fields = True
    warn_unsaved_form = True
    list_filter_sheet = False
    change_form_show_cancel_button = True

    # Actions
    actions_row = ["edit"]

    # Custom fields
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {"widget": ArrayWidget},
    }

    @action(
        description=_("Edit"),
        permissions=["edit"],
        url_path="edit-post",
    )
    def edit(self, request: HttpRequest, object_id: int):
        """Redirect to the change form for this object."""
        return redirect(
            reverse(
                f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change",
                args=[object_id],
            )
        )

    def has_edit_permission(self, request, obj=None):
        """
        Check if the user has permission to edit.
        Usually, this maps to the standard 'change' permission.
        """
        return self.has_change_permission(request, obj)

    # Pagination
    paginator = InfinitePaginator
