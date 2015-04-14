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
from registrar.models import CourseSetting

# View
from teacher.views import setting

# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "ContinentalUnion"
TEST_USER_EMAIL2 = "whalesquid@hideauze.com"
TEST_USER_USERNAME2 = "whalesquid"
TEST_USER_PASSWORD2 = "Evolvers"

# Notes:
# https://docs.djangoproject.com/en/1.7/topics/testing/tools/#assertions

# Create your tests here.
class SettingsTestCase(TestCase):
    def tearDown(self):
        courses = Course.objects.all()
        for course in courses:
            course.delete()
        User.objects.all().delete()
    
    def setUp(self):
        # Create our Trudy user.
        User.objects.create_user(
            email=TEST_USER_EMAIL2,
            username=TEST_USER_USERNAME2,
            password=TEST_USER_PASSWORD2
        )
        user = User.objects.get(email=TEST_USER_EMAIL2)
        teacher = Teacher.objects.create(user=user)
                                 
        # Create our Student.
        user = User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        teacher = Teacher.objects.create(user=user)
        course = Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
            teacher=teacher,
        )
        CourseSetting.objects.create(
            settings_id=1,
            course=course,
        )

    def get_logged_in_client(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        return client

    def test_url_resolves_to_announcements_page_view(self):
        found = resolve('/teacher/course/1/settings')
        self.assertEqual(found.func, setting.settings_page)

    def test_settings_page_without_submissions(self):
        try:
            CourseSetting.objects.get(settings_id=1).delete()
        except CourseSetting.DoesNotExist:
            pass
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/settings')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)

    def test_settings_page_with_submissions(self):
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/settings')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)

    def test_suspend_course(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/suspend_course',{}, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'changed')
        self.assertEqual(array['status'], 'success')
