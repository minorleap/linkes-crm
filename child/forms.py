from django import forms
from .models import Child


class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = (
            'client', 'relationship_to_client', 'active', 'first_name', 'last_name', 'date_of_birth', 'gender', 'pronouns',
            'school', 'school_class', 'activities_consent', 'photography_consent', 'is_peer_volunteer', 'languages_spoken',
            'has_no_disability', 'has_physical_impairment', 'has_sensory_impairment', 'has_learning_disability',
            'has_mental_health_condition', 'has_any_other_disability', 'disability_details', 'notes',
        )
        widgets = {
            'date_of_birth': forms.TextInput(attrs={'placeholder':'dd/mm/yyyy'}),
            'client': forms.HiddenInput(attrs={'readonly':'readonly'}),
        }
        labels = {
            "notes": "",
            "languages_spoken": "",
            "is_peer_volunteer": "Peer volunteer",
            "school_class": "Class",
            "has_no_disability": "No disability or impairment",
            "has_physical_impairment": "Physical impairment",
            "has_sensory_impairment": "Sensory impairment",
            "has_learning_disability": "Learning disability",
            "has_mental_health_condition": "Mental health condition",
            "has_any_other_disability": "Any other disability or impairment",
        }
