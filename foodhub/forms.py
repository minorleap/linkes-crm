from django import forms
from .models import FoodhubCollection
import datetime


class FoodhubCollectionForm(forms.ModelForm):
    class Meta:
        model = FoodhubCollection
        date = forms.DateField(input_formats=['%d/%m/%Y'])
        fields = (
            'client', 'date', 'number_of_adults', 'number_of_children', 'allergies', 'diabetic', 'gluten_free',
            'dairy_free', 'vegetarian', 'vegan', 'halal', 'notes',
        )
        widgets = {
            'client': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }
        labels = {'number_of_children': 'Number of CYP'}

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        client = cleaned_data.get("client")
        if  self.instance.pk == None and FoodhubCollection.objects.filter(client=client, date=date):
            msg = "This client already has a collection recorded on this date"
            self.add_error('date', msg)
