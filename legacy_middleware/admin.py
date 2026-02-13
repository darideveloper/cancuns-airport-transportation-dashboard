from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import LegacyAPIToken

# Register your models here.


@admin.register(LegacyAPIToken)
class LegacyAPITokenAdmin(SingletonModelAdmin):
    pass
