from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from landpage.views import txt
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
        
    def test_robots_txt_page(self):
        found = resolve('/robots.txt');
        self.assertEqual(found.func,txt.robots_txt_page)

    def test_humans_txt_page(self):
        found = resolve('/humans.txt');
        self.assertEqual(found.func,txt.humans_txt_page)
