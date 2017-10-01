from django import forms

from edc_base.modelform_validators import FormValidator
from edc_constants.constants import YES, NO


class MovedMemberFormValidator(FormValidator):

    def clean(self):

        self.required_if(
            YES,
            field='moved_community',
            field_required='new_community')

        self.not_applicable_if(
            YES,
            field='has_moved',
            field_applicable='details_change_reason'
        )

        self.not_applicable_if(
            YES,
            field='has_moved',
            field_applicable='inability_to_participate'
        )

        self.not_applicable_if(
            YES,
            field='has_moved',
            field_applicable='study_resident'
        )

        self.not_applicable_if(
            YES,
            field='has_moved',
            field_applicable='personal_details_changed'
        )

        self.not_applicable_if(
            YES,
            field='has_moved',
            field_applicable='personal_details_changed'
        )

        self.not_applicable_if(
            NO,
            field='present_today',
            field_applicable='inability_to_participate'
        )

        self.not_applicable_if(
            NO,
            field='present_today',
            field_applicable='study_resident'
        )

        self.not_applicable_if(
            NO,
            field='present_today',
            field_applicable='personal_details_changed'
        )

        self.not_applicable_if(
            NO,
            field='present_today',
            field_applicable='details_change_reason'
        )

        self.not_applicable_if(
            YES,
            field='has_moved',
            field_applicable='inability_to_participate'
        )

        self.not_applicable_if(
            YES,
            field='has_moved',
            field_applicable='study_resident'
        )

        self.not_applicable_if(
            YES,
            field='has_moved',
            field_applicable='personal_details_changed'
        )

        if self.instance.id and self.instance.has_moved not in [YES] and self.instance.present_today not in [NO]:
            raise forms.ValidationError(
                'Household Member does not indicate that this member has moved',
                code='household_member_has_moved')
