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
from registrar.models import Student
from registrar.models import CourseFinalMark
from registrar.views import enrolment


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class EnrolmentTestCase(TestCase):
    def setUp(self):
        # Create our user.
        User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user = User.objects.get(email=TEST_USER_EMAIL)
        teacher = Teacher.objects.create(user=user)
        student = Student.objects.create(user=user)
                                 
        # Create a test course
        course = Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
            teacher=teacher,
        )
                                 
        # Create our announcement(s)
        CourseFinalMark.objects.create(
            credit_id=1,
            percent=75,
            is_public=True,
            course=course,
            student=student,
        )
    
    def test_url_resolves_to_transcript_page_view(self):
        found = resolve('/enrolment')
        self.assertEqual(found.func, enrolment.enrolment_page)
    
    def test_transcript_page_with_no_enrolments(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/enrolment')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Become a Student!',response.content)

    def test_transcript_page_with_enrolments(self):
        user = User.objects.get(email=TEST_USER_EMAIL)
        student = Student.objects.get(user=user)
        course = Course.objects.get(id=1)
        course.students.add(student)
        course.save()
        
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/enrolment')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'ajax_continue_course(1);',response.content)

