from django import forms
from .models import FoodbankReferral
import datetime


class FoodbankReferralForm(forms.ModelForm):
    class Meta:
        model = FoodbankReferral
        date = forms.DateField(input_formats=['%d/%m/%Y'])
        fields = (
            'client', 'date',
        )
        widgets = {
            'client': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }
