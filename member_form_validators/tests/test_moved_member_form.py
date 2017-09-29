from member.forms import MovedMemberForm
from member.tests import MemberTestHelper
from member.tests import TestMapper

from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.utils import tag
from edc_constants.constants import YES, NO
from survey.tests import SurveyTestHelper

from edc_map.site_mappers import site_mappers

from ..form_validators.moved_member import MovedMemberFormValidator


class TestMovedMemberFormValidator(TestCase):

    member_helper = MemberTestHelper()
    survey_helper = SurveyTestHelper()

    def setUp(self):
        self.survey_helper.load_test_surveys()
        django_apps.app_configs['edc_device'].device_id = '99'
        site_mappers.registry = {}
        site_mappers.loaded = False
        site_mappers.register(TestMapper)
        report_datetime = self.member_helper.get_utcnow()
        household_structure = self.member_helper.make_household_ready_for_enumeration(
            report_datetime=report_datetime)
        self.household_member = self.member_helper.add_household_member(
            household_structure=household_structure,
            report_datetime=report_datetime)

    def test_form(self):
        form = MovedMemberForm()
        self.assertFalse(form.is_valid())

    def test_household_member_moved(self):
        cleaned_data = dict(
            moved_household=YES,
            moved_community=NO,
            update_locator=YES)
        form_validator = MovedMemberFormValidator(
            cleaned_data=cleaned_data,
            instance=self.household_member)
        self.assertRaises(forms.ValidationError, form_validator.validate)

    def test_moved_community_with_new_community(self):
        cleaned_data = dict(
            has_moved=YES,
            update_locator=YES,
            moved_community=YES,
            new_community=None)
        form_validator = MovedMemberFormValidator(
            cleaned_data=cleaned_data, instance=self.household_member)
        self.assertRaises(forms.ValidationError, form_validator.validate)
        self.assertIn('new_community', form_validator._errors)

    def test_moved_household_none_moved_community(self):
        cleaned_data = dict(
            has_moved=YES,
            update_locator=YES,
            moved_household=YES,
            moved_community=None)
        form_validator = MovedMemberFormValidator(
            cleaned_data=cleaned_data, instance=self.household_member)
        self.assertRaises(forms.ValidationError, form_validator.validate)
        self.assertIn('moved_community', form_validator._errors)
