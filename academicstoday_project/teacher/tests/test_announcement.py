# Django & Python
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json

# Modal
from registrar.models import Course
from registrar.models import Teacher
from registrar.models import Announcement

# View
from teacher.views import announcement

# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"

# Notes:
# https://docs.djangoproject.com/en/1.7/topics/testing/tools/#assertions

# Create your tests here.
class AnnouncementTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        Teacher.objects.create(user=user)
        course = Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
        )
        Announcement.objects.create(
            announcement_id=1,
            course=course,
            title='Hello world!',
            body='This is the body of the message.',
        )

    def get_logged_in_client(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        return client

    def test_url_resolves_to_announcements_page_view(self):
        found = resolve('/teacher/course/1/announcement')
        self.assertEqual(found.func, announcement.announcements_page)

    def test_announcements_page_without_submissions(self):
        try:
            Announcement.objects.get(announcement_id=1).delete()
        except Announcement.DoesNotExist:
            pass
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/announcement')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'ajax_announcement_modal(0);',response.content)

    def test_announcements_page_with_submissions(self):
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/announcement')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'Hello world!',response.content)
        self.assertIn(b'This is the body of the message.',response.content)

    def test_announcements_table_without_submissions(self):
        try:
            Announcement.objects.get(announcement_id=1).delete()
        except Announcement.DoesNotExist:
            pass
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/announcements_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ajax_announcement_modal(0);',response.content)
    
    def test_announcements_table_with_submissions(self):
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/announcements_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello world!',response.content)
        self.assertIn(b'This is the body of the message.',response.content)

    def test_announcement_modal_without_submissions(self):
        try:
            Announcement.objects.get(announcement_id=1).delete()
        except Announcement.DoesNotExist:
            pass
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/announcement_modal',{
            'announcement_id': 0,
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'announcement_modal',response.content)

    def test_announcement_modal_with_submissions(self):
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/announcement_modal',{
            'announcement_id': 1,
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'announcement_modal',response.content)


    def test_save_announcement_with_insert(self):
        try:
            Announcement.objects.get(announcement_id=1).delete()
        except Announcement.DoesNotExist:
            pass
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/save_announcement',{
            'announcement_id': 0,
            'title': 'test',
            'body': 'test',
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')

    def test_save_announcement_with_update(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/save_announcement',{
            'announcement_id': 1,
            'title': 'test',
            'body': 'test',
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')

    def test_delete_announcement_without_record(self):
        try:
            Announcement.objects.get(announcement_id=1).delete()
        except Announcement.DoesNotExist:
            pass
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/delete_announcement',{
            'announcement_id': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'cannot find record')
        self.assertEqual(array['status'], 'failed')

    def test_delete_announcement_with_record(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/delete_announcement',{
            'announcement_id': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'deleted')
        self.assertEqual(array['status'], 'success')
