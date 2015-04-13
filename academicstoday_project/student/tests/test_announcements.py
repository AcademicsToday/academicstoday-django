from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from registrar.models import Course
from registrar.models import Teacher
from registrar.models import Announcement
from student.views import announcement


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class AnnouncementTestCase(TestCase):
    def tearDown(self):
        Announcement.objects.all().delete()
        courses = Course.objects.all()
        for course in courses:
            course.delete()
        User.objects.get(email=TEST_USER_EMAIL).delete()

    def setUp(self):
        # Create our user.
        User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user = User.objects.get(email=TEST_USER_EMAIL)
        teacher = Teacher.objects.create(user=user)

        # Create a test course
        course = Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
            teacher=teacher,
        )

        # Create our announcement(s)
        Announcement.objects.create(
            course=course,
            title='Hello world!',
            body='This is the body of the message.',
        )


    def test_url_resolves_to_announcements_page_view(self):
        found = resolve('/course/1/announcements')
        self.assertEqual(found.func, announcement.announcements_page)


    def test_announcements_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/course/1/announcements')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'Hello world!',response.content)
        self.assertIn(b'This is the body of the message.',response.content)
