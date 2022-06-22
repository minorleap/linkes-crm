import django_filters
from django import forms
from .models import Staff, Timesheet


class StaffFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control'}))
    postcode = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'postcode',]


class TimesheetsFilter(django_filters.FilterSet):
    week_commencing = django_filters.DateFilter(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control text-center',
            }
        )
    )
    class Meta:
        model = Timesheet
        fields = ['week_commencing',]
