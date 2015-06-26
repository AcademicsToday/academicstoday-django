import json
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import views

# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "ContinentalUnion"


class LoginTestCase(TestCase):
    """
        python manage.py test login
    """
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
    
    def test_root_url_resolves_to_login_modal_view(self):
        found = resolve('/login_modal')
        self.assertEqual(found.func,views.login_modal)
    
    def test_login_modal_returns_correct_html(self):
        client = Client()
        response = client.post('/login_modal')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.startswith(b'<div'))
        self.assertIn(b'login_modal',response.content)
        self.assertIn(b'loginForm',response.content)    
    
    def test_login_authentication_with_succesful_login(self):
        # Extra parameters to make this a Ajax style request.
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        
        # Test
        client = Client()
        response = client.post(
            '/login',
            {'username': TEST_USER_USERNAME, 'password': TEST_USER_PASSWORD},
            **kwargs
        )
        
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'logged on')


    def test_login_authentication_with_failed_login(self):
        # Extra parameters to make this a Ajax style request.
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        
        # Test
        client = Client()
        response = client.post(
            '/login',
            {'username': TEST_USER_USERNAME, 'password': 'wrong_password'},
            **kwargs
        )
            
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                               
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'failure')
        self.assertEqual(array['message'], 'wrong username or password')

    def test_login_authentication_with_suspension(self):
        # Extra parameters to make this a Ajax style request.
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
     
        # Suspend User
        user = User.objects.get(username=TEST_USER_USERNAME)
        user.is_active = False
        user.save()
   
        # Test
        client = Client()
        response = client.post(
            '/login',
            {'username': TEST_USER_USERNAME, 'password': TEST_USER_PASSWORD},
            **kwargs
        )
            
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                               
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'failure')
        self.assertEqual(array['message'], 'you are suspended')

    def test_logout_authentication_with_success(self):
        # Extra parameters to make this a Ajax style request.
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        
        # Test
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/logout', {}, **kwargs )
            
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                               
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'you are logged off')

    def test_login_authentication_with_non_ajax_call(self):
        # Test
        client = Client()
        response = client.post(
            '/login',
            {'username': TEST_USER_USERNAME, 'password': TEST_USER_PASSWORD}
        )
            
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                               
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'failure')
        self.assertEqual(array['message'], 'an unknown error occured')

    def test_logout_authentication_with_non_ajax_call(self):
        # Test
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/logout')
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
                     
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'you are logged off')
