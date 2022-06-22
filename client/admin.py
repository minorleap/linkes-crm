from django.contrib import admin
from .models import Client, Referral, Casenote

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'address1', 'address2', 'postcode', 'active', 'health_status',)
    list_filter = ('active', 'health_status',)
    search_fields = ('postcode', 'last_name', 'first_name',)
    ordering = ('last_name', 'first_name', 'postcode',)

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('client', 'referred_to', 'referred_to_other', 'date',)
    list_filter = ('referred_to',)
    date_hierarchy = 'date'
    ordering = ('-date',)

@admin.register(Casenote)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('client', 'date', 'notes')
    list_filter = ('client',)
    date_hierarchy = 'date'
    ordering = ('-date',)
