from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .models import CalendarDay, Medication, Perception


class CalendarDayForm(forms.ModelForm):
    class Meta:
        model = CalendarDay
        exclude = ()
        widgets = {
            "medication": forms.CheckboxSelectMultiple(),
        }
        labels = {
            "medication": "",
        }

    def __init__(self, date, *args, **kwargs):
        super(CalendarDayForm, self).__init__(*args, **kwargs)
        field = self.fields['date']
        field.widget = field.hidden_widget()
        field.initial = date.date()

        f1 = Q( days__number=date.weekday() )
        f_enddate_is_none = Q( enddate__isnull = True )
        f_enddate_is_not_none = Q( enddate__gt=date.date() )

        self.fields['medication'].queryset = Medication.objects.filter( f1 & ( f_enddate_is_none | f_enddate_is_not_none ) )  
        calendar_day = CalendarDay.objects.filter(date=date).first()
        if calendar_day is not None:
            self.fields['medication'].initial = calendar_day.medication

    # this function will be used for the validation
    def clean(self):
        super(CalendarDayForm, self).clean()
        return self.cleaned_data


class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        exclude = ("creation_date",)
        widgets = {
            "days": forms.CheckboxSelectMultiple(),
            "time": forms.CheckboxSelectMultiple(),
            "enddate": forms.TextInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(MedicationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(Field('name', placeholder=""), css_class='form-group col-md-6 mb-0'),
                Column(Field('type', placeholder=""), css_class='form-group col-md-6 mb-0'),
                css_class='form-row align-items-center'
            ),
            Row(
                Column(Field('amount', placeholder=""), css_class='form-group col-md-6 mb-0'),
                Column(Field('dosage', placeholder=""), css_class='form-group col-md-6 mb-0'),
                css_class='form-row align-items-center'
            ),
            Row(
                Column(Field('days', placeholder=""), css_class='form-group col-md-6 mb-0'),
                Column(Field('enddate', placeholder=""), Field('time', placeholder=""), css_class='form-group col-md-6 mb-0'),
                css_class='form-row align-items-center'
            ),
        )

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


class MedicationSearchForm(forms.Form):
    search_text = forms.CharField(max_length=64, label="", required=False)

    def __init__(self, *args, **kwargs):
        super(MedicationSearchForm, self).__init__(*args, **kwargs)
    
    # this function will be used for the validation
    def clean(self):
        super(MedicationSearchForm, self).clean()
        return self.cleaned_data
