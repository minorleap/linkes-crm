from django import forms
from .models import ShoppingCollection, ShoppingSchedule, ExceptionDate, MissedCollectionDate
import datetime


class ShoppingCollectionForm(forms.ModelForm):
    class Meta:
        model = ShoppingCollection
        date = forms.DateField(input_formats=['%d/%m/%Y'])
        fields = (
            'type', 'client', 'date', 'time', 'number_of_adults', 'number_of_children', 'dietary_requirements',
        )
        widgets = {
            'client': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'type': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }
        labels = {'number_of_children': 'Number of CYP'}

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise forms.ValidationError('Collection date must be in the future')
            date = datetime.date.today()
        return date

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        client = cleaned_data.get("client")

        if  self.instance.pk == None and ShoppingCollection.objects.filter(client=client, date=date):
            msg = "This client already has a collection scheduled on this date"
            self.add_error('date', msg)

        if hasattr(client, 'halal_shopping_schedule') and client.halal_shopping_schedule.exception_dates.filter(date=date):
            msg = "The client has requested to skip this date."
            self.add_error('date', msg)



class ShoppingScheduleForm(forms.ModelForm):
    class Meta:
        model = ShoppingSchedule
        start_date = forms.DateField(input_formats=['%d/%m/%Y'])
        end_date = forms.DateField(input_formats=['%d/%m/%Y'])
        fields = (
            'client', 'status', 'number_of_adults', 'number_of_children', 'start_date', 'end_date', 'time',
            'allergies', 'diabetic', 'gluten_free', 'dairy_free', 'vegetarian', 'vegan',
        )
        widgets = {
            'client': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }
        labels = {'allergies': 'Allergic to', 'number_of_children': 'Number of CYP'}


class ExceptionDateForm(forms.ModelForm):
    class Meta:
        model = ExceptionDate
        date = forms.DateField(input_formats=['%d/%m/%Y'])
        fields = ('date', 'schedule',)
        widgets = {
            'schedule': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise forms.ValidationError('Exception date must be in the future')
            date = datetime.date.today()
        return date

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        schedule = cleaned_data.get("schedule")

        if schedule.exception_dates.filter(date=date):
            msg = "This exception date has already been added to the schedule."
            self.add_error('date', msg)


class MissedCollectionDateForm(forms.ModelForm):
    class Meta:
        model = MissedCollectionDate
        date = forms.DateField(input_formats=['%d/%m/%Y'])
        fields = ('date', 'schedule', 'notes',)
        widgets = {
            'schedule': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > datetime.date.today():
            raise forms.ValidationError('Missed collection date must be in the past')
            date = datetime.date.today()
        return date

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        schedule = cleaned_data.get("schedule")

        if schedule.missed_collection_dates.filter(date=date):
            msg = "This missed collection date has already been added to the schedule."
            self.add_error('date', msg)
