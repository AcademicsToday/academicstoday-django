from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static, settings
import json
from registrar.models import Course
from registrar.models import Teacher
from registrar.models import Student
from registrar.models import Syllabus
from student.views import syllabus


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class SyllabusTestCase(TestCase):
    def tearDown(self):
        syllabuses = Syllabus.objects.all()
        for syllabus in syllabuses:
            syllabus.delete()
        courses = Course.objects.all()
        for course in courses:
            course.delete()
        User.objects.get(email=TEST_USER_EMAIL).delete()

    def setUp(self):
        # Create our Student.
        User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user = User.objects.get(email=TEST_USER_EMAIL)
        teacher = Teacher.objects.create(user=user)
        Student.objects.create(user=user).save()
                                 
        # Create a test course.
        Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
            teacher=teacher,
        )

    def get_logged_in_client(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        return client

    def test_url_resolves_to_syllabus_page_view(self):
        found = resolve('/course/1/syllabus')
        self.assertEqual(found.func, syllabus.syllabus_page)

    def test_syllabus_page_with_correct_html(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/syllabus')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'<h1>Syllabus</h1>',response.content)