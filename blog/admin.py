from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpRequest
from django.contrib import messages
from django.shortcuts import redirect

from unfold.decorators import action

from project.admin import ModelAdminUnfoldBase
from utils.media import get_media_url
from blog import models as models


@admin.register(models.Post)
class PostAdmin(ModelAdminUnfoldBase):
    # Django basic setup
    list_display = ("title", "lang", "created_at")
    search_fields = ("title", "description", "content")
    list_filter = ("lang",)


@admin.register(models.Image)
class ImageAdmin(ModelAdminUnfoldBase):
    list_display = ("name", "image")
    search_fields = ("name",)
    ordering = ("name",)

    # This will now be merged with ["edit"] automatically
    actions_row = ["copy_link"]

    @action(description="Copiar link")
    def copy_link(self, request: HttpRequest, object_id: int):
        obj = self.get_object(request, object_id)

        # Get url and show message
        image_url = get_media_url(obj.image.url)
        messages.success(request, f"Copiado al portapapeles: {image_url}")

        # Redirect to the same page with a cookie
        response = redirect(request.META.get("HTTP_REFERER", ".."))
        response.set_cookie("copy_to_clipboard", image_url, max_age=10)

        return response

    class Media:
        js = ("js/copy_clipboard.js",)
