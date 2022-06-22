from django import forms
from .models import Phonecall, PhonecallSchedule, ExceptionDate, MissedCallDate, PhonecallNotes
import datetime


class PhonecallForm(forms.ModelForm):
    class Meta:
        model = Phonecall
        date = forms.DateField(input_formats=['%d/%m/%Y'])
        fields = (
            'type', 'client', 'date', 'time_of_day'
        )
        widgets = {
            'client': forms.HiddenInput(attrs={'readonly':'readonly'}),
            'type': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise forms.ValidationError('Date must be in the future')
            date = datetime.date.today()
        return date

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        client = cleaned_data.get("client")

        if  self.instance.pk == None and Phonecall.objects.filter(client=client, date=date):
            msg = "This client already has a phone call scheduled on this date"
            self.add_error('date', msg)

        if hasattr(client, 'phonecall_schedule') and client.phonecall_schedule.exception_dates.filter(date=date):
            msg = "The client has requested to skip this date."
            self.add_error('date', msg)



class PhonecallScheduleForm(forms.ModelForm):
    class Meta:
        model = PhonecallSchedule
        start_date = forms.DateField(input_formats=['%d/%m/%Y'])
        end_date = forms.DateField(input_formats=['%d/%m/%Y'])
        fields = (
            'client', 'status', 'start_date', 'end_date', 'weekday', 'time_of_day', 'frequency'
        )
        widgets = {
            'client': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }


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


class MissedCallDateForm(forms.ModelForm):
    class Meta:
        model = MissedCallDate
        date = forms.DateField(input_formats=['%d/%m/%Y'])
        fields = ('date', 'schedule', 'notes',)
        widgets = {
            'schedule': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > datetime.date.today():
            raise forms.ValidationError('Missed call date cannot be in the fututre')
            date = datetime.date.today()
        return date

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        schedule = cleaned_data.get("schedule")

        if schedule.missed_call_dates.filter(date=date):
            msg = "This missed call date has already been added to the schedule."
            self.add_error('date', msg)


class PhonecallNotesForm(forms.ModelForm):
    class Meta:
        model = PhonecallNotes
        date = forms.DateField(input_formats=['%d/%m/%Y'])
        fields = ('date', 'schedule', 'notes',)
        widgets = {
            'schedule': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > datetime.date.today():
            raise forms.ValidationError('The date of the phone call cannot be in the future')
            date = datetime.date.today()
        return date
