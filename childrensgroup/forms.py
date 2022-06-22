from django import forms
from .models import GroupType, Group, GroupSession, GroupBooking
import datetime


class GroupTypeForm(forms.ModelForm):
    class Meta:
        model = GroupType
        fields = (
            'name',
        )


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        start_date = forms.DateField(input_formats=['%d/%m/%Y'])
        end_date = forms.DateField(input_formats=['%d/%m/%Y'])
        fields = (
            'active', 'group_type', 'start_date', 'end_date', 'capacity',
        )
        widgets = {
            'group_type': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }

    def clean_end_date(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        if start_date > end_date:
            raise forms.ValidationError('The end date must be after the start date')
        return end_date

    def clean_capacity(self):
        capacity = self.cleaned_data['capacity']
        min_capacity = len(self.instance.bookings.all())
        if capacity < min_capacity:
            raise forms.ValidationError('There are currently ' + str(min_capacity) + ' bookings')
        return capacity


class GroupSessionForm(forms.ModelForm):
    class Meta:
        model = GroupSession
        date = forms.DateField(input_formats=['%d/%m/%Y'])
        fields = (
            'group', 'date', 'time',
        )
        widgets = {
            'group': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        group = self.cleaned_data['group']
        if group.start_date > date:
            raise forms.ValidationError('Date cannot be before the group\'s start date')
        if group.end_date < date:
            raise forms.ValidationError('Date cannot be after the group\'s end date')
        return date


class BulkGroupSessionForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), widget=forms.HiddenInput())
    start_date = forms.DateField(required=True)
    end_date = forms.DateField(required=True)
    time = forms.TimeField(required=True)
    monday = forms.BooleanField(required=False)
    tuesday = forms.BooleanField(required=False)
    wednesday = forms.BooleanField(required=False)
    thursday = forms.BooleanField(required=False)
    friday = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data['start_date']
        end_date = cleaned_data['end_date']
        the_group = self.cleaned_data['group']
        if start_date > end_date:
            msg = 'The start date cannot be after the end date'
            self.add_error('start_date', msg)
        if start_date < the_group.start_date:
            msg = 'The start date cannot be before the group\'s start date'
            self.add_error('start_date', msg)
        if start_date > the_group.end_date:
            msg = 'The start date cannot be after the group\'s end date'
            self.add_error('start_date', msg)
        if end_date > the_group.end_date:
            msg = 'The end date cannot be after the group\'s end date'
            self.add_error('end_date', msg)
        if end_date < the_group.start_date:
            msg = 'The end date cannot be before the group\'s start date'
            self.add_error('end_date', msg)


class GroupBookingForm(forms.ModelForm):
    class Meta:
        model = GroupBooking
        fields = (
            'group', 'child',
        )
        widgets = {
            'child': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(GroupBookingForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.filter(active=True)

    def clean_group(self):
        group = self.cleaned_data['group']
        if not group.get_remaining_capacity():
            raise forms.ValidationError('This group is full')
        return group
