from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . import views
import json
from landpage.models import LandpageTeamMember
from landpage.models import LandpageCoursePreview
from registrar.models import Course
from registrar.models import Student
from registrar.models import Teacher


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class LandpageTest(TestCase):
    def tearDown(self):
        courses = Course.objects.all()
        for course in courses:
            course.delete()
        User.objects.get(email=TEST_USER_EMAIL).delete()
    
    def setUp(self):
        User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user = User.objects.get(email=TEST_USER_EMAIL)
        teacher = Teacher.objects.create(user=user)
        student = Student.objects.create(user=user)
        course = Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
            teacher=teacher,
        )

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func,views.landpage_page)

    def test_robots_txt_page(self):
        found = resolve('/robots.txt');
        self.assertEqual(found.func,views.robots_txt_page)

    def test_humans_txt_page(self):
        found = resolve('/humans.txt');
        self.assertEqual(found.func,views.humans_txt_page)

    def test_landpage_page(self):
        found = resolve('/landpage');
        self.assertEqual(found.func,views.landpage_page)

# Example of using HttpRequest
#    def test_course_preview_returns_corret_html(self):
#        request = HttpRequest()
#        request.POST = QueryDict('course_preview_id=1')
#        response = views.course_preview_modal(request)
#
#        # Validate
#        print(response.content)
#        self.assertIn(b'<form',response.content)

    def test_course_preview_modal_returns_correct_html(self):
        parameters = {"course_id":1}
        client = Client()
        response = client.post(
            '/course_preview_modal',
            data=parameters,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'The definitive course on comics!',response.content)

    def test_login_modal_returns_correct_html(self):
        client = Client()
        response = client.post('/login_modal')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.startswith(b'<div'))
        self.assertIn(b'login_modal',response.content)
        self.assertIn(b'loginForm',response.content)

    def test_register_modal_returns_correct_html(self):
        client = Client()
        response = client.post('/register_modal')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.startswith(b'<div'))
        self.assertIn(b'register_modal',response.content)
        self.assertIn(b'register_form',response.content)
