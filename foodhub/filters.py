import django_filters
from django import forms
from .models import FoodhubCollection
import datetime


class FoodhubCollectionFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control text-center',
            }
        )
    )
    class Meta:
        model = FoodhubCollection
        fields = ['date',]
