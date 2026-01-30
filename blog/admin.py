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


from blog import models as blog_models
from project.admin import ModelAdminUnfoldBase


@admin.register(blog_models.Post)
class PostAdmin(ModelAdminUnfoldBase):
    # Django basic setup
    list_display = ("title", "lang", "created_at")
    search_fields = ("title", "description", "content")
    list_filter = ("lang",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
