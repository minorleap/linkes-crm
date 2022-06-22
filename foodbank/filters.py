import django_filters
from django import forms
from .models import FoodbankReferral
import datetime


class FoodbankReferralFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control text-center',
            }
        )
    )
    class Meta:
        model = FoodbankReferral
        fields = ['date',]
