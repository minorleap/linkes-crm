from django.contrib import admin
from .models import FoodbankReferral

@admin.register(FoodbankReferral)
class FoodbankReferralAdmin(admin.ModelAdmin):
    list_display = ('client', 'date',)
    list_filter = ('client', 'date',)
    ordering = ('date',)
