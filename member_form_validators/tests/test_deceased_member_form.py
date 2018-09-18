from django.apps import apps as django_apps
from django.test import TestCase, tag
from model_mommy import mommy

from edc_base.utils import get_utcnow
from edc_map.site_mappers import site_mappers
from member.forms import DeceasedMemberForm
from member.models import HouseholdMember
from member.tests import MemberTestHelper, TestMapper
from survey.tests import SurveyTestHelper


@tag('dsc')
class TestHouseholdMemberFormValidator(TestCase):

    member_helper = MemberTestHelper()
    survey_helper = SurveyTestHelper()

    def setUp(self):
        self.survey_helper.load_test_surveys()
        django_apps.app_configs['edc_device'].device_id = '99'
        site_mappers.registry = {}
        site_mappers.loaded = False
        site_mappers.register(TestMapper)
        self.household_structure = self.member_helper.make_household_ready_for_enumeration(
            make_hoh=False)
        self.today_datetime = self.household_structure.report_datetime
        self.household_member = self.member_helper.add_household_member(self.household_structure)
        
        self.options = {
            'household_member':self.household_member.id,
            'report_datetime':get_utcnow(),
            'survey_schedule': self.household_structure.survey_schedule,
            'death_date': get_utcnow().date(),
            'site_aware_date': get_utcnow().date(),
            'death_cause': 'Natural',
            'duration_of_illness':60,
            'relationship_death_study': 'Definitely not related',
            'extra_death_info': 'blah blah',
            'extra_death_info_date': get_utcnow(),
        }

    def test_form(self):
        form = DeceasedMemberForm(data=self.options)
        self.assertTrue(form.is_valid())
    
    def test_extra_death_info_date_valid(self):
        self.options.update(extra_death_info_date=None)
        form = DeceasedMemberForm(data=self.options)
        self.assertFalse(form.is_valid())
        self.assertIn('extra_death_info_date', form._errors)
        
        
    
    
    