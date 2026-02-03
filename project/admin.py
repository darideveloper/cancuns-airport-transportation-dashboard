from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from django.contrib import admin
from django.db import models
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.decorators import action
from unfold.paginator import InfinitePaginator
from unfold.contrib.filters.admin import RangeDateFilter
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin


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


# Base class for all admin models
class ModelAdminUnfoldBase(ModelAdmin):
    # ---------------------------------------------------------------------------
    # Django default setup
    # ---------------------------------------------------------------------------
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    # ---------------------------------------------------------------------------
    # UI setup
    # ---------------------------------------------------------------------------
    compressed_fields = True
    warn_unsaved_form = True
    list_filter_sheet = False
    change_form_show_cancel_button = True

    # ---------------------------------------------------------------------------
    # Actions
    # ---------------------------------------------------------------------------
    actions_row = ["edit"]

    def _get_base_actions_row(self):
        """
        Overriding Unfold internal logic to merge strings.
        This ensures Unfold receives a list of strings it can resolve itself.
        """
        base_actions = ["edit"]
        child_actions = getattr(self, "actions_row", [])

        # Merge unique string names
        all_actions = base_actions + [a for a in child_actions if a not in base_actions]

        # Call the original method logic but with our merged list
        return [self.get_unfold_action(action) for action in all_actions]

    @action(
        description="Editar",
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

    # ---------------------------------------------------------------------------
    # Custom fields / widgets
    # ---------------------------------------------------------------------------
    base_formfield_overrides = {
        # models.TextField: {"widget": WysiwygWidget},
    }

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        # Apply base overrides first
        for klass in db_field.__class__.mro():
            if klass in self.base_formfield_overrides:
                kwargs.update(self.base_formfield_overrides[klass])
                break
        # Let Django handle the standard 'formfield_overrides' (from child classes)
        # This will naturally overwrite base settings if the same field class is used.
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    # ---------------------------------------------------------------------------
    # Pagination
    # ---------------------------------------------------------------------------
    paginator = InfinitePaginator

    # ---------------------------------------------------------------------------
    # Filters
    # ---------------------------------------------------------------------------
    global_filters = (
        ("created_at", RangeDateFilter),
        ("updated_at", RangeDateFilter),
    )

    def get_list_filter(self, request):
        # Get filters defined in the child class
        child_filters = super().get_list_filter(request) or []

        # Create a list to hold our final filters
        final_filters = list(child_filters)

        # Only add global filters if the model actually has those fields
        model_fields = [f.name for f in self.model._meta.get_fields()]

        for field_name, filter_class in self.global_filters:
            if field_name in model_fields and field_name not in str(final_filters):
                final_filters.append((field_name, filter_class))

        return final_filters
