from django.contrib import admin
from .models import PhonecallSchedule, Phonecall, ExceptionDate, MissedCallDate, PhonecallNotes

@admin.register(PhonecallSchedule)
class PhonecallScheduleAdmin(admin.ModelAdmin):
    list_display = ('status', 'start_date', 'end_date', 'time_of_day', 'frequency')
    list_filter = ('status',)
    ordering = ('-created',)


@admin.register(Phonecall)
class PhonecallAdmin(admin.ModelAdmin):
    list_display = ('date', 'time_of_day',)
    date_hierarchy = 'date'
    ordering = ('-date', 'time_of_day')


@admin.register(ExceptionDate)
class ExceptionDateAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'date',)
    ordering = ('-created',)


@admin.register(MissedCallDate)
class MissedCallDateAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'date',)
    ordering = ('-created',)


@admin.register(PhonecallNotes)
class PhonecallNotesAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'date',)
    ordering = ('-created',)
