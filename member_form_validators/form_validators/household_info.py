from django import forms
from django.apps import apps as django_apps
from edc_base.modelform_validators import FormValidator
from django.core.exceptions import ObjectDoesNotExist


class HouseholdInfoFormValidator(FormValidator):

    representative_eligibility_model = 'member.representativeeligibility'

    def clean(self):
        representative_eligibility_model_cls = django_apps.get_model(
            self.representative_eligibility_model)
        try:
            representative_eligibility_model_cls.objects.get(
                household_structure=self.cleaned_data.get('household_structure'))
        except ObjectDoesNotExist:
            verbose_name = representative_eligibility_model_cls._meta.verbose_name
            raise forms.ValidationError(
                f'Please complete {verbose_name} first.')

        self.validate_other_specify('flooring_type')
        self.validate_other_specify('water_source')
        self.validate_other_specify('energy_source')
        self.validate_other_specify('toilet_facility')
