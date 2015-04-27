from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from landpage.views import terms
import json
from landpage.models import LandpageTeamMember
from landpage.models import LandpageCoursePreview
from registrar.models import Course
from registrar.models import Student
from registrar.models import Teacher


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class TermsTest(TestCase):
    def tearDown(self):
        pass
    
    def setUp(self):
        pass

    def test_url_resolves_to_terms_page(self):
        found = resolve('/terms');
        self.assertEqual(found.func,terms.terms_page)

    def test_terms_page_returns_correct_html(self):
        parameters = {"course_id":1}
        client = Client()
        response = client.post(
            '/terms',
            data=parameters,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Terms',response.content)
#        self.assertIn(b'The definitive course on comics!',response.content)
