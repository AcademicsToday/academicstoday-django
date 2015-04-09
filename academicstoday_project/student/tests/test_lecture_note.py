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
from registrar.models import Lecture
from registrar.models import FileUpload
from student.views import lecture_note


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class LectureNoteTestCase(TestCase):
    def tearDown(self):
        courses = Course.objects.all()
        for course in courses:
            course.delete()
        uploads = FileUpload.objects.all()
        for upload in uploads:
            upload.delete()
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
        student = Student.objects.create(user=user)
                                 
        # Create a test course.
        Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
            teacher=teacher,
        )
        course = Course.objects.get(id=1)
        Lecture.objects.create(
            lecture_id=1,
            lecture_num=1,
            week_num=1,
            title="Blade vs Evil",
            description="Fighting for the destiny of the Earth.",
            course=course,
        )

    def get_logged_in_client(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        return client
    
    def test_url_resolves_to_lectures_page_view(self):
        found = resolve('/course/1/lecture/1/notes')
        self.assertEqual(found.func, lecture_note.lecture_notes_page)
    
    def test_lecture_notes_page(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/lecture/1/notes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'Lectures',response.content)

    def test_url_resolves_to_lecture_note_modal(self):
        found = resolve('/course/1/lecture/1/view_lecture_note')
        self.assertEqual(found.func, lecture_note.view_lecture_note)

    def test_lecture_note_modal(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/course/1/lecture/1/view_lecture_note',{
            'upload_id': 1,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'lecture_modal',response.content)