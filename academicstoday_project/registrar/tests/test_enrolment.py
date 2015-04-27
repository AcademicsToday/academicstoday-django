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
from registrar.views import enrollment


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class EnrollmentTestCase(TestCase):
    def tearDown(self):
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
    
    def test_url_resolves_to_enrollment_page_view(self):
        found = resolve('/enrollment')
        self.assertEqual(found.func, enrollment.enrollment_page)
    
    def test_enrollment_page_with_no_enrollments(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/enrollment')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Become a Student!',response.content)

    def test_enrollment_page_with_enrollments(self):
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
        response = client.post('/enrollment')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'ajax_continue_course(1);',response.content)

    def test_url_resolves_to_disenroll_modal_view(self):
        found = resolve('/disenroll_modal')
        self.assertEqual(found.func, enrollment.disenroll_modal)

    def test_disenroll_modal_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = client.post('/disenroll_modal', {
            'course_id': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warning',response.content)

    def test_url_resolves_to_disenroll_view(self):
        found = resolve('/disenroll')
        self.assertEqual(found.func, enrollment.disenroll)

    def test_disenroll_with_no_enrollment(self):
        # Delete courses
        courses = Course.objects.all()
        for course in courses:
            course.delete()
        
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = client.post('/disenroll', {
            'course_id': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'record does not exist')
        self.assertEqual(array['status'], 'failed')

    def test_disenroll_with_enrollment(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = client.post('/disenroll', {
            'course_id': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'disenrolled')
        self.assertEqual(array['status'], 'success')
