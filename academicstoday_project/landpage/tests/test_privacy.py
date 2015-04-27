from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from landpage.views import privacy
import json
from landpage.models import LandpageTeamMember
from landpage.models import LandpageCoursePreview
from registrar.models import Course
from registrar.models import Student
from registrar.models import Teacher


class PrivacyTest(TestCase):
    def tearDown(self):
        pass
    
    def setUp(self):
        pass
    
    def test_url_resolves_to_privacy_page(self):
        found = resolve('/privacy');
        self.assertEqual(found.func,privacy.privacy_page)

    def test_privacy_page_returns_correct_html(self):
        parameters = {"course_id":1}
        client = Client()
        response = client.post(
            '/privacy',
            data=parameters,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Privacy',response.content)
        self.assertIn(b'(1)',response.content)
