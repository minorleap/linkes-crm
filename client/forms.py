from django import forms
from .models import Client, Referral, Casenote


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            'first_name', 'last_name', 'address1', 'address2', 'address3', 'town', 'postcode', 'active', 'health_status',
            'phone', 'email', 'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation', 'gdpr_consent',
            'gdpr_consent_giver', 'notes', 'date_of_birth', 'gender', 'gender_specify', 'pronouns', 'has_disability',
            'physical_impairment', 'sensory_impairment', 'mental_health_condition', 'learning_disability', 'hiv_cancer_ms',
            'ethnicity_category', 'ethnicity_white', 'ethnicity_asian', 'ethnicity_african', 'ethnicity_other', 'ethnicity_specify',
            'has_caring_responsibilities', 'primary_carer_child', 'primary_carer_disabled_child', 'primary_carer_disabled_adult', 'primary_carer_older_person',
            'secondary_carer', 'married', 'sexual_orientation', 'sexual_orientation_specify', 'religion', 'religion_specify',
            'first_language', 'nationality', 'country_of_origin',
        )
        widgets = {
            'date_of_birth': forms.TextInput(attrs={'placeholder':'dd/mm/yyyy'}),
        }
        labels = {
            "emergency_contact_name": "Name",
            "emergency_contact_phone": "Phone",
            "emergency_contact_relation": "Relation to client",
            "address1": "Address 1",
            "address2": "Address 2",
            "address3": "Address 3",
            "gdpr_consent": "GDPR consent",
            "gdpr_consent_giver": "Consent given on behalf by",
            "has_disability": "Has a disability",
            "notes": "",
            "hiv_cancer_ms": "Diagnosed as HIV positive, or with cancer or multiple sclerosis",
            "married": "Married or in a civil partnership",
            "sexual_orientation": "Sexual orientation",
            "sexual_orientation_specify": "Specify other sexual orientation",
            "ethnicity_white": "Ethnicity",
            "ethnicity_asian": "Ethnicity",
            "ethnicity_african": "Ethnicity",
            "ethnicity_other": "Ethnicity",
            "ethnicity_specify": "Specify other ethnicity",
            "gender_specify": "Specify other gender",
            "religion": "Religion or belief",
            "religion_specify": "Specify other religion",
        }

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data['first_name']
        last_name = cleaned_data['last_name']
        address1 = cleaned_data['address1']
        postcode = cleaned_data['postcode']
        gdpr_consent = cleaned_data.get("gdpr_consent")
        gdpr_consent_giver = cleaned_data.get("gdpr_consent_giver")
        emergency_contact_name = cleaned_data['emergency_contact_name']
        emergency_contact_phone = cleaned_data['emergency_contact_phone']
        emergency_contact_relation = cleaned_data['emergency_contact_relation']
        ethnicity_category = cleaned_data['ethnicity_category']
        ethnicity_white = cleaned_data['ethnicity_white']
        ethnicity_asian = cleaned_data['ethnicity_asian']
        ethnicity_african = cleaned_data['ethnicity_african']
        ethnicity_other = cleaned_data['ethnicity_other']
        ethnicity_specify = cleaned_data['ethnicity_specify']
        religion = cleaned_data['religion']
        religion_specify = cleaned_data['religion_specify']
        sexual_orientation = cleaned_data['sexual_orientation']
        sexual_orientation_specify = cleaned_data['sexual_orientation_specify']

        if  self.instance.pk == None and Client.objects.filter(first_name=first_name, last_name=last_name, address1=address1, postcode=postcode):
            msg = "A client with this name and address already exists"
            self.add_error('first_name', msg)
            self.add_error('last_name', msg)
            self.add_error('address1', msg)
            self.add_error('postcode', msg)

        if gdpr_consent == 'given_on_behalf' and not gdpr_consent_giver:
            msg = 'Please state who provided consent on behalf of the client'
            self.add_error('gdpr_consent_giver', msg)

        if emergency_contact_name and not emergency_contact_phone:
            msg = 'Please enter a phone number for the emergency contact'
            self.add_error('emergency_contact_phone', msg)

        if emergency_contact_name and not emergency_contact_relation:
            msg = 'Please specify the contact\'s relation to the client (e.g. support worker)'
            self.add_error('emergency_contact_relation', msg)

        if ethnicity_category == 'mixed' \
        or ethnicity_white == 'other' \
        or ethnicity_asian == 'other' \
        or ethnicity_african == 'other' \
        or ethnicity_other == 'other' \
        and not ethnicity_specify:
            msg = 'Please specify the client\'s ethnicity'
            self.add_error('ethnicity_specify', msg)

        if ethnicity_category == 'white' and not ethnicity_white:
            msg = 'Please specify the client\'s ethnicity'
            self.add_error('ethnicity_white', msg)

        if ethnicity_category == 'asian' and not ethnicity_asian:
            msg = 'Please specify the client\'s ethnicity'
            self.add_error('ethnicity_asian', msg)

        if ethnicity_category == 'african' and not ethnicity_african:
            msg = 'Please specify the client\'s ethnicity'
            self.add_error('ethnicity_african', msg)

        if ethnicity_category == 'other' and not ethnicity_other:
            msg = 'Please specify the client\'s ethnicity'
            self.add_error('ethnicity_other', msg)

        if religion == 'other' and not religion_specify:
            msg = 'Please specify the client\'s religion'
            self.add_error('religion_specify', msg)

        if sexual_orientation == 'other' and not sexual_orientation_specify:
            msg = 'Please specify the client\'s sexual orientation'
            self.add_error('sexual_orientation_specify', msg)


class ReferralForm(forms.ModelForm):
    class Meta:
        model = Referral
        fields = ('referred_to', 'referred_to_other', 'client', 'date')
        widgets = {
            'client': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }
        labels = {'referred_to_other': 'Specify other'}

    def clean(self):
        cleaned_data = super().clean()
        referred_to = cleaned_data['referred_to']
        referred_to_other = cleaned_data['referred_to_other']
        if referred_to == 'other' and not referred_to_other:
            msg = 'Please specify which organisation the client was referred to'
            self.add_error('referred_to_other', msg)


class CasenoteForm(forms.ModelForm):
    class Meta:
        model = Casenote
        fields = ('date', 'notes', 'client')
        widgets = {
            'client': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }
