from django.contrib import admin
from .models import ShoppingSchedule, ShoppingCollection, ExceptionDate, MissedCollectionDate

@admin.register(ShoppingSchedule)
class ShoppingScheduleAdmin(admin.ModelAdmin):
    list_display = ('status', 'number_of_adults', 'number_of_children', 'start_date', 'end_date', 'time')
    list_filter = ('status',)
    ordering = ('-created',)


@admin.register(ShoppingCollection)
class ShoppingCollectionAdmin(admin.ModelAdmin):
    list_display = ('date', 'number_of_adults', 'number_of_children', 'dietary_requirements', 'time',)
    date_hierarchy = 'date'
    ordering = ('-date',)


@admin.register(ExceptionDate)
class ExceptionDateAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'date',)
    ordering = ('-created',)


@admin.register(MissedCollectionDate)
class MissedCollectionDateAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'date',)
    ordering = ('-created',)
