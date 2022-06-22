from django.contrib import admin
from .models import FoodhubCollection


@admin.register(FoodhubCollection)
class FoodhubCollectionAdmin(admin.ModelAdmin):
    list_display = ('date', 'client', 'number_of_adults', 'number_of_children',)
    date_hierarchy = 'date'
    ordering = ('-date',)
