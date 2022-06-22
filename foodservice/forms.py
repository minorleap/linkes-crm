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
        fields = (
            'name', 'active', 'group_type', 'capacity',
        )
        widgets = {
            'group_type': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }

    def clean_capacity(self):
        capacity = self.cleaned_data['capacity']
        min_capacity = self.instance.get_places_booked()
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


class GroupBookingForm(forms.ModelForm):
    class Meta:
        model = GroupBooking
        fields = (
            'group', 'client', 'active', 'number_of_adults', 'number_of_children', 'allergies', 'diabetic', 'gluten_free',
            'dairy_free', 'vegetarian', 'vegan', 'halal', 'notes',
        )
        widgets = {
            'client': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(GroupBookingForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.filter(active=True)

    def clean(self):
        cleaned_data = super().clean()
        active = cleaned_data['active']
        group = cleaned_data['group']
        # don't reactivate a booking if there is no capacity
        if not group.get_remaining_capacity() and active and not self.instance.active:
            msg = 'This group is full'
            self.add_error('group', msg)
        # don't create a new booking if there is no capacity
        elif not group.get_remaining_capacity() and active:
            msg = 'This group is full'
            self.add_error('group', msg)
