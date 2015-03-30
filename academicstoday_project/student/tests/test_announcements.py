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
from registrar.models import Announcement

# View
from student.views import announcement

# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"

# Notes:
# https://docs.djangoproject.com/en/1.7/topics/testing/tools/#assertions

# Create your tests here.
class AnnouncementTestCase(TestCase):
    def setUp(self):
        # Create our user.
        User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        ).save()

        # Create a test course
        Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
        ).save()
        
        course = Course.objects.get(id=1)
        if course is None:
            self.assertTrue(False)

        # Create our announcement(s)
        Announcement.objects.create(
            course=course,
            title='Hello world!',
            body='This is the body of the message.',
        ).save()


    def test_url_resolves_to_announcements_page_view(self):
        found = resolve('/course/1/announcement')
        self.assertEqual(found.func, announcement.announcements_page)


    def test_announcements_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/course/1/announcement')
        
        # Verify we are in the correct course.
        self.assertIn(b'Comics Book Course',response.content)
        
        # Verify our announcement was listed.
        self.assertIn(b'Hello world!',response.content)
        self.assertIn(b'This is the body of the message.',response.content)
