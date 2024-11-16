from django import forms

from .models import Medication, Perception


class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        exclude = ()
        widgets = {}

    def __init__(self, *args, **kwargs):
        super(MedicationForm, self).__init__(*args, **kwargs)

    # this function will be used for the validation
    def clean(self):
        super(MedicationForm, self).clean()
        return self.cleaned_data


class PerceptionForm(forms.ModelForm):
    class Meta:
        model = Perception
        fields = ['health',]
        widgets = {}

    def __init__(self, *args, **kwargs):
        super(PerceptionForm, self).__init__(*args, **kwargs)
    
    # this function will be used for the validation
    def clean(self):
        super(PerceptionForm, self).clean()
        return self.cleaned_data
