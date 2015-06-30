from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from landpage.views import google
import json


class GoogleVerifyTest(TestCase):
    """
        python manage.py test landpage.tests.test_google
    """
    def tearDown(self):
        pass
    
    def setUp(self):
        pass
    
    def test_url_resolves_to_google_verify_page_view(self):
        found = resolve('/googlee81f1c16590924d1.html')
        self.assertEqual(found.func,google.google_verify_page)

    def test_google_verify_page_returns_correct_html(self):
        client = Client()
        response = client.post(
            '/googlee81f1c16590924d1.html',
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'googlee81f1c16590924d1.html',response.content)
