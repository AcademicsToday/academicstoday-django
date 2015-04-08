from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from account.views import setting


# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class SettingTestCase(TestCase):
    def tearDown(self):
        User.objects.get(email=TEST_USER_EMAIL).delete()

    def setUp(self):
        # Create our user.
        user = User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user.is_active = True
        user.save()

    def test_url_resolves_to_settings_page_view(self):
        found = resolve('/settings')
        self.assertEqual(found.func, setting.settings_page)

    def test_settings_page_with_success(self):
        # Extra parameters to make this a Ajax style request.
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        
        # Test
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/settings',{}, **kwargs)
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        
        # Verify: Check that donation content was returned.
        self.assertIn(b'New Password',response.content)
        self.assertIn(b'Repeat New Password',response.content)

    def test_update_password_success(self):
        # Extra parameters to make this a Ajax style request.
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
            
        # Test
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/update_password',{
            'password': 'Transhumanism',
            'repeat_password': 'Transhumanism',
            'old_password': TEST_USER_PASSWORD,
        }, **kwargs)
                                      
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                                      
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'updated password')
