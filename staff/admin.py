from django.contrib import admin
from .models import Staff, Role, Timesheet

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    list_filter = ('active',)
    search_fields = ('last_name', 'first_name',)
    ordering = ('last_name', 'first_name',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('staff', 'name',)
    list_filter = ('name',)
    ordering = ('name',)


@admin.register(Timesheet)
class TimesheetAdmin(admin.ModelAdmin):
    list_display = ('staff', 'role', 'week_commencing', 'total_hours')
    list_filter = ('staff', 'role',  'week_commencing')
    ordering = ('week_commencing', 'role', 'staff')
