from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from account.views import donate

# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class DonateTestCase(TestCase):
    def tearDown(self):
        User.objects.get(email=TEST_USER_EMAIL).delete()

    def setUp(self):
        # Create our user.
        user = User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user.save()

    def test_url_resolves_to_donate_page_view(self):
        found = resolve('/donate')
        self.assertEqual(found.func, donate.donate_page)
    
    def test_donate_page_returns_correct_html(self):
        # Test
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/donate')
        
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        
        # Verify: Check that donation content was returned.
        self.assertIn(b'PayPal',response.content)
        self.assertIn(b'Bitcoin',response.content)
