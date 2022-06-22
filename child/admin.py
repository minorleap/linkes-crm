from django.contrib import admin
from .models import Child

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth',)
    list_filter = ('active',)
    search_fields = ('last_name', 'first_name',)
    ordering = ('last_name', 'first_name',)
