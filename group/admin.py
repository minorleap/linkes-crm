from django.contrib import admin
from .models import GroupType, Group, GroupSession, GroupBooking

@admin.register(GroupType)
class GroupTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_type', 'start_date', 'end_date', 'capacity', 'creche_capacity', 'active',)
    list_filter = ('active', 'start_date', 'end_date')
    ordering = ('-start_date', 'group_type',)


@admin.register(GroupSession)
class GroupSessionAdmin(admin.ModelAdmin):
    list_display = ('group', 'date', 'time',)
    list_filter = ('group', 'date', 'time')
    ordering = ('group', '-date', '-time')


@admin.register(GroupBooking)
class GroupBookingAdmin(admin.ModelAdmin):
    list_display = ('group', 'client', 'creche_spaces', 'names_of_children',)
    list_filter = ('group',)
    ordering = ('group', 'client',)
