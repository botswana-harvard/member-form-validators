from django import forms

from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES, NO


class MovedMemberFormValidator(FormValidator):

    def clean(self):

        self.required_if(
            YES,
            field='moved_community',
            field_required='new_community')

        self.required_if(
            YES,
            field='moved_household',
            field_required='moved_community')

        if self.instance.id and self.instance.has_moved not in [YES]:
            raise forms.ValidationError(
                'Household Member does not indicate that this member has moved',
                code='household_member_has_moved')
