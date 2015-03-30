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
from registrar.models import Assignment
from registrar.models import Student

# View
from student.views import assignment

# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"

# Notes:
# https://docs.djangoproject.com/en/1.7/topics/testing/tools/#assertions

# Create your tests here.
class AssignmentTestCase(TestCase):
    def setUp(self):
        # Create our Student.
        User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        ).save()
        user = User.objects.get(email=TEST_USER_EMAIL)
        Student.objects.create(user=user).save()
        
        # Create a test course.
        Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
        ).save()
        
        course = Course.objects.get(id=1)
        if course is None:
            self.assertTrue(False)

        # Create our assignment(s)
        Assignment.objects.create(
            assignment_id=1,
            assignment_num=1,
            title="Hideauze",
            description="Anime related assignment.",
            worth=25,
            course=course,
        ).save()

    def get_logged_in_client(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        return client

    def test_url_resolves_to_assignments_page_view(self):
        found = resolve('/course/1/assignments')
        self.assertEqual(found.func, assignment.assignments_page)

    def test_assignments_page_returns_correct_html(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/assignments')

        # Verify we are in the correct course.
        self.assertIn(b'Comics Book Course',response.content)
        
        # Verify our assignment was listed.
        self.assertIn(b'view_assignment(1);',response.content)

    def test_url_resolves_to_assignment_table_view(self):
        found = resolve('/course/1/assignments_table')
        self.assertEqual(found.func, assignment.assignments_table)

    def test_assignments_table_returns_correct_html(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/assignments_table')
        
        # Verify our assignment was listed.
        self.assertIn(b'view_assignment(1);',response.content)
    
    def test_url_resolves_to_delete_assignment(self):
        found = resolve('/course/1/delete_assignment')
        self.assertEqual(found.func, assignment.delete_assignment)
    
    def test_delete_assignment_returns_correct_json(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/course/1/delete_assignment',{
            'assignment_id': 1,
        }, **kwargs)
        
        # Verify
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'assignment was deleted')

    def test_url_resolves_to_assignment_page_view(self):
        found = resolve('/course/1/assignment/1')
        self.assertEqual(found.func, assignment.assignment_page)
