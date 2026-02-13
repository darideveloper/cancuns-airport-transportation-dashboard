from django.contrib import admin
from solo.admin import SingletonModelAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from .models import LegacyAPIToken


@admin.register(LegacyAPIToken)
class LegacyAPITokenAdmin(UnfoldModelAdmin, SingletonModelAdmin):
    # This combines Unfold's UI with Solo's singleton logic
    pass
