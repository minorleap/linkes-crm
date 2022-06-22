import django_filters
from django import forms
from .models import ShoppingCollection
import datetime


class ShoppingCollectionFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control text-center',
            }
        )
    )
    class Meta:
        model = ShoppingCollection
        fields = ['date',]
