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
from registrar.models import CourseFinalMark
from registrar.views import courses


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class TeachingTestCase(TestCase):
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
        Teacher.objects.create(user=user)
        Student.objects.create(user=user)
            
    def test_url_resolves_to_courses_page_view(self):
        found = resolve('/courses')
        self.assertEqual(found.func, courses.courses_page)
            
    def test_courses_page_without_courses(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/courses')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b' <h1>Courses Unavailable</h1>',response.content)

    def test_courses_page_with_courses(self):
        user = User.objects.get(email=TEST_USER_EMAIL)
        teacher = Teacher.objects.get(user=user)
        Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
            teacher=teacher,
            status=settings.COURSE_AVAILABLE_STATUS,
        )
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/courses')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'ajax_enroll(1);',response.content)

    def test_url_resolves_to_enroll(self):
        found = resolve('/enroll')
        self.assertEqual(found.func, courses.enroll)

    def test_enroll(self):
        user = User.objects.get(email=TEST_USER_EMAIL)
        teacher = Teacher.objects.get(user=user)
        student = Student.objects.get(user=user)
        Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
            teacher=teacher,
            status=settings.COURSE_AVAILABLE_STATUS,
        )
        
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = client.post('/enroll',{
            'course_id': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'enrolled')
        self.assertEqual(array['status'], 'success')