import django_filters
from django import forms
from .models import Client


class ClientFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control'}))
    postcode = django_filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'postcode',]
