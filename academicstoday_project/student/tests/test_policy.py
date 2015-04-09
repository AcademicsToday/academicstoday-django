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
from registrar.models import Policy
from student.views import policy


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class PolicyTestCase(TestCase):
    def tearDown(self):
        policies = Policy.objects.all()
        for policy in policies:
            policy.delete()
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

    def test_url_resolves_to_policy_page_view(self):
        found = resolve('/course/1/policy')
        self.assertEqual(found.func, policy.policy_page)
    
    def test_policy_page_with_correct_html(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/policy')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'<h1>Policy and Grades</h1>',response.content)