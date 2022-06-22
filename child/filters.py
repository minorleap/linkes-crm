import django_filters
from django import forms
from .models import Child
import datetime


class ChildFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control'}))
    school = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control'}))
    min_age = django_filters.NumberFilter(field_name='date_of_birth', method='get_past_n_years', label='Min Age', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_age = django_filters.NumberFilter(field_name='date_of_birth', method='get_next_n_years', label='Max Age', widget=forms.NumberInput(attrs={'class': 'form-control'}))


    def get_past_n_years(self, queryset, field_name, value):
        days = int(365 * value)
        n_years_ago = datetime.date.today() - datetime.timedelta(days=days)
        return queryset.filter(date_of_birth__lte=n_years_ago)

    def get_next_n_years(self, queryset, field_name, value):
        days = int(365 * value)
        n_years_ago = datetime.date.today() - datetime.timedelta(days=days+365)
        return queryset.filter(date_of_birth__gte=n_years_ago)

    class Meta:
        model = Child
        fields = ['first_name', 'last_name', 'school', 'min_age', 'max_age']
