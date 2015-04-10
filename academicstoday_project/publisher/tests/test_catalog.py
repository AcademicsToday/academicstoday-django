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
from registrar.views import certificate


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class CertificateTestCase(TestCase):
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

    def test_url_resolves_to_certificate_page_view(self):
        found = resolve('/certificates')
        self.assertEqual(found.func, certificate.certificates_page)
    
    def test_certificate_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/certificates')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'view_1_btn',response.content)
        self.assertIn(b'certificate/1',response.content)

    def test_url_resolves_to_certificate_table_view(self):
        found = resolve('/certificates_table')
        self.assertEqual(found.func, certificate.certificates_table)
    
    def test_certificate_table_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/certificates_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'view_1_btn',response.content)
        self.assertIn(b'certificate/1',response.content)

    def test_url_resolves_to_certificate_view(self):
        found = resolve('/certificate/1')
        self.assertEqual(found.func, certificate.certificate_page)
    
    def test_certificate_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/certificate/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Certificate of Completion</h1>',response.content)

    def test_url_resolves_to_certificate_permalink_modal(self):
        found = resolve('/certificate_permalink_modal')
        self.assertEqual(found.func, certificate.certificate_permalink_modal)
    
    def test_certificate_permalink_modal_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/certificate_permalink_modal', { 'credit_id': 1, })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'permalink_modal',response.content)
        self.assertIn(b'http://www.academicstoday.ca/certificate/1',response.content)

    def test_change_certificate_accessiblity(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = client.post('/change_certificate_accessiblity', { 'credit_id': 1, }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'certificate accessiblity changed')

