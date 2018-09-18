from edc_base.modelform_validators import FormValidator


class DeceasedMemberFormValidator(FormValidator):

    def clean(self):
        
        self.required_if_not_none(
            field='extra_death_info',
            field_required='extra_death_info_date'
        )
