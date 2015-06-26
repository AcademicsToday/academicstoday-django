from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from . import views
from captcha.models import CaptchaStore

# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class RegistrationTestCase(TestCase):
    """
        python manage.py test registration
    """
    def tearDown(self):
        User.objects.all().delete()
    
    def setUp(self):
        captcha_count = CaptchaStore.objects.count()
        self.failUnlessEqual(captcha_count, 0)

    def test_url_resolves_to_register(self):
        found = resolve('/register')
        self.assertEqual(found.func, views.register)

    def test_register_with_succesful_login(self):
        # Extra parameters to make this a Ajax style request.
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        
        # Developer Notes:
        # To get unit tests working with the django-simple-captcha then follow:
        # http://stackoverflow.com/questions/3159284/how-to-unit-test-a-form-with-a-captcha-field-in-django
        
        # Test
        client = Client()
        response = client.post('/register',{
            'username': TEST_USER_USERNAME,
            'password': TEST_USER_PASSWORD,
            'password_repeated': TEST_USER_PASSWORD,
            'first_name': 'Ledo',
            'last_name': 'Dunno',
            'email': TEST_USER_EMAIL,
            'is_18_or_plus': True,
            'captcha_0': 'dummy-value',
            'captcha_1': 'PASSED',
        },**kwargs)
        
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'user registered')
        self.assertEqual(array['status'], 'success')

        # Verify: Database updated
        try:
            user = User.objects.get(email=TEST_USER_EMAIL)
        except User.DoesNotExist:
            user = None
        self.assertEqual(user.username, TEST_USER_EMAIL)