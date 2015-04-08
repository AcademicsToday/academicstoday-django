from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from account.views import profile


# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class ProfileTestCase(TestCase):
    def tearDown(self):
        User.objects.all().delete()
    
    def setUp(self):
        # Create our user.
        user = User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user.is_active = True
        user.save()

    def test_url_resolves_to_profile_page_view(self):
        found = resolve('/profile')
        self.assertEqual(found.func, profile.profile_page)

    def test_profile_page_with_success(self):
        # Extra parameters to make this a Ajax style request.
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        
        # Test
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/profile',{}, **kwargs)
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        
        # Verify: Check that donation content was returned.
        self.assertIn(b'Email',response.content)
        self.assertIn(b'Profile',response.content)

    def test_update_user_with_success(self):
        # Extra parameters to make this a Ajax style request.
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
            
        # Test
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/update_user',{
            'first_name': 'Evolver',
            'last_name': '1234',
            'email': 'whalesquid@hideauze.com',
        }, **kwargs)
                                      
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                                      
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'updated user')

        # Verfiy: Updated in database
        try:
            user = User.objects.get(email="whalesquid@hideauze.com")
        except User.DoesNotExist:
            user = None
        self.assertEqual(user.first_name, 'Evolver')
        self.assertEqual(user.last_name, '1234')
