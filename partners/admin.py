# Register your models here.

from django.contrib import admin
from .models import Partner


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')


admin.site.register(Partner, PartnerAdmin)
