import django_filters
from django import forms
from .models import Phonecall
import datetime


class PhonecallFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control text-center',
            }
        )
    )
    class Meta:
        model = Phonecall
        fields = ['date',]
