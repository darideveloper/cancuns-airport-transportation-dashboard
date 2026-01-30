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
    list_display = ("title", "slug", "author", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title", "content")
    # prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('author',)
    # date_hierarchy = 'publish'
    # ordering = ('status', 'publish')
    list_display_links = ("title", "slug")
