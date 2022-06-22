from django.contrib import admin
from .models import ShoppingSchedule, ShoppingDelivery, ExceptionDate, MissedDeliveryDate

@admin.register(ShoppingSchedule)
class ShoppingScheduleAdmin(admin.ModelAdmin):
    list_display = ('status', 'number_of_adults', 'number_of_children', 'start_date', 'end_date',)
    list_filter = ('status',)
    ordering = ('-created',)


@admin.register(ShoppingDelivery)
class ShoppingDeliveryAdmin(admin.ModelAdmin):
    list_display = ('date', 'number_of_adults', 'number_of_children', 'dietary_requirements', 'delivery_notes',)
    date_hierarchy = 'date'
    ordering = ('-date',)


@admin.register(ExceptionDate)
class ExceptionDateAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'date',)
    ordering = ('-created',)


@admin.register(MissedDeliveryDate)
class MissedDeliveryDateAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'date',)
    ordering = ('-created',)
