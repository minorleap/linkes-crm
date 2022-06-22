from django.contrib import admin
from .models import GroupType, Group, GroupSession, GroupBooking

@admin.register(GroupType)
class GroupTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_type', 'name', 'capacity', 'active',)
    list_filter = ('active',)
    ordering = ('group_type',)


@admin.register(GroupSession)
class GroupSessionAdmin(admin.ModelAdmin):
    list_display = ('group', 'date', 'time',)
    list_filter = ('group', 'date', 'time')
    ordering = ('group', '-date', '-time')


@admin.register(GroupBooking)
class GroupBookingAdmin(admin.ModelAdmin):
    list_display = ('group', 'client', 'active',)
    list_filter = ('group', 'active',)
    ordering = ('active', 'group', 'client',)
