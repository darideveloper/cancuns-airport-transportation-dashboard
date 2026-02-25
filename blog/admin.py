from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpRequest
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import JSONField

from unfold.decorators import action
from unfold.admin import display
from unfold.contrib.forms.widgets import ArrayWidget

from project.admin import ModelAdminUnfoldBase
from utils.media import get_media_url
from blog import models as models


@admin.register(models.Post)
class PostAdmin(ModelAdminUnfoldBase):
    # Django basic setup
    list_display = ("title", "lang", "created_at")
    search_fields = ("title", "description", "content")
    list_filter = ("lang",)

    # Custom js
    class Media:
        js = ("js/load_markdown.js",)


@admin.register(models.Image)
class ImageAdmin(ModelAdminUnfoldBase):
    list_display = ("name", "created_at", "display_image")
    search_fields = ("name",)
    ordering = ("name",)

    # actions
    actions_row = ["copy_link"]

    @action(description="Copy link")
    def copy_link(self, request: HttpRequest, object_id: int):
        obj = self.get_object(request, object_id)

        # Get url and show message
        image_url = get_media_url(obj.image.url)
        messages.success(request, f"Copied to clipboard: {image_url}")

        # Redirect to the same page with a cookie
        response = redirect(request.META.get("HTTP_REFERER", ".."))
        response.set_cookie("copy_to_clipboard", image_url, max_age=10)

        return response

    # Custom js
    class Media:
        js = ("js/copy_clipboard.js",)

    # Custom fields
    @display(description="Preview")
    def display_image(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" class="img-preview" />')
        return None
        
    def has_module_permission(self, request):
        # The model still exists, but won't show up in the sidebar or index
        return False
