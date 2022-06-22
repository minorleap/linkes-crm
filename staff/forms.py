from django import forms
from django.forms import modelformset_factory
from .models import Staff, Role, Timesheet


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = (
            'first_name', 'last_name', 'address1', 'address2', 'address3', 'town', 'postcode', 'active',
            'phone', 'email', 'notes',
        )
        labels = {
            "address1": "Address 1",
            "address2": "Address 2",
            "address3": "Address 3",
            "notes": "",
        }

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data['first_name']
        last_name = cleaned_data['last_name']
        address1 = cleaned_data['address1']
        postcode = cleaned_data['postcode']

        if  self.instance.pk == None and Staff.objects.filter(first_name=first_name, last_name=last_name, address1=address1, postcode=postcode):
            msg = "A staff member with this name and address already exists"
            self.add_error('first_name', msg)
            self.add_error('last_name', msg)
            self.add_error('address1', msg)
            self.add_error('postcode', msg)


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ('name', 'staff',)
        widgets = {
            'staff': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }

class TimesheetForm(forms.ModelForm):
    class Meta:
        model = Timesheet
        fields = ('staff', 'role', 'week_commencing', 'monday_hours', 'tuesday_hours', 'wednesday_hours', 'thursday_hours', 'friday_hours', 'saturday_hours')
        widgets = {
            'staff': forms.widgets.Select(attrs={'class':'form-control'}),
            'role': forms.widgets.Select(attrs={'class':'form-control'}),
            'week_commencing': forms.widgets.TextInput(attrs={'class':'form-control'}),
            'monday_hours': forms.widgets.TextInput(attrs={'class':'form-control'}),
            'tuesday_hours': forms.widgets.TextInput(attrs={'class':'form-control'}),
            'wednesday_hours': forms.widgets.TextInput(attrs={'class':'form-control'}),
            'thursday_hours': forms.widgets.TextInput(attrs={'class':'form-control'}),
            'friday_hours': forms.widgets.TextInput(attrs={'class':'form-control'}),
            'saturday_hours': forms.widgets.TextInput(attrs={'class':'form-control'}),
        }


TimesheetFormSet = modelformset_factory(Timesheet, form=TimesheetForm)
