from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from account.models import PrivateMessage
from account.views import mail

# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class PrivateMessagingTestCase(TestCase):
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

    def test_url_resolves_to_mail_page_view(self):
        found = resolve('/inbox')
        self.assertEqual(found.func, mail.mail_page)

    def test_send_private_messaging_with_success(self):
        # Extra parameters to make this a Ajax style request.
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}

        # Test
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/send_private_message',{
            'title': 'Hello World',
            'message': 'This is a test',
            'email': TEST_USER_EMAIL,
        }, **kwargs)

        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'private message sent')

    def test_view_private_message_with_success(self):
        # Extra parameters to make this a Ajax style request.
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        
        # Pre-load test data
        PrivateMessage.objects.create(
            id=1,
            title='Hello World',
            text='This is a test',
            to_address=TEST_USER_EMAIL,
            from_address=TEST_USER_EMAIL,
        )
        
        # Test
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/view_private_message',{
            'message_id': 1,
        }, **kwargs)
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        
        # Verify: Check that donation content was returned.
        self.assertIn(b'Hello World',response.content)
        self.assertIn(b'This is a test',response.content)

    def test_delete_private_message_with_success(self):
        # Extra parameters to make this a Ajax style request.
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        
        # Pre-load test data
        PrivateMessage.objects.create(
            id=1,
            title='Hello World',
            text='This is a test',
            to_address=TEST_USER_EMAIL,
            from_address=TEST_USER_EMAIL,
        )
        
        # Test
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/delete_private_message',{
            'message_id': 1,
        }, **kwargs)
                     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
            
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'deleted private message')
