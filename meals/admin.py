from django.contrib import admin
from .models import MealsSchedule, MealsDelivery, ExceptionDate, MissedDeliveryDate

@admin.register(MealsSchedule)
class MealsScheduleAdmin(admin.ModelAdmin):
    list_display = ('status', 'number_of_adults', 'number_of_children', 'start_date', 'end_date', 'monday_delivery', 'wednesday_delivery', 'friday_delivery',)
    list_filter = ('status', 'monday_delivery', 'wednesday_delivery', 'friday_delivery',)
    ordering = ('-created',)


@admin.register(MealsDelivery)
class MealsDeliveryAdmin(admin.ModelAdmin):
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
