# Register your models here.

from django.contrib import admin
from .models import Clickthrough


class ClickthroughAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'merchant_wine', 'partner')
    list_filter = ('timestamp', 'merchant_wine', 'partner')


admin.site.register(Clickthrough, ClickthroughAdmin)
