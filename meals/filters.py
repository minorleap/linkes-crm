import django_filters
from django import forms
from .models import MealsDelivery
import datetime


class MealsDeliveryFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control text-center',
            }
        )
    )
    class Meta:
        model = MealsDelivery
        fields = ['date',]
