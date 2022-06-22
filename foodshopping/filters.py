import django_filters
from django import forms
from .models import ShoppingDelivery
import datetime


class ShoppingDeliveryFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control text-center',
            }
        )
    )
    class Meta:
        model = ShoppingDelivery
        fields = ['date',]
