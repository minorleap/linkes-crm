import django_filters
from django import forms
from django.db import models
from .models import Group, GroupSession
import datetime


class GroupFilter(django_filters.FilterSet):
    class Meta:
        model = Group
        fields = ['group_type']


class GroupSessionFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control text-center',
            }
        )
    )
    class Meta:
        model = GroupSession
        fields = ['date',]
