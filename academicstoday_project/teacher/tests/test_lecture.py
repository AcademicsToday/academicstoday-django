# Django & Python
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

# Modal
from registrar.models import Course
from registrar.models import Teacher
from registrar.models import Lecture


# View
from teacher.views import lecture

# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "ContinentalUnion"
TEST_USER_EMAIL2 = "whalesquid@hideauze.com"
TEST_USER_USERNAME2 = "whalesquid"
TEST_USER_PASSWORD2 = "Evolvers"

# Notes:
# https://docs.djangoproject.com/en/1.7/topics/testing/tools/#assertions

# Create your tests here.
class LectureTestCase(TestCase):
    def tearDown(self):
        courses = Course.objects.all()
        for course in courses:
            course.delete()
        User.objects.all().delete()

    def setUp(self):
        # Create our Trudy user.
        User.objects.create_user(
            email=TEST_USER_EMAIL2,
            username=TEST_USER_USERNAME2,
            password=TEST_USER_PASSWORD2
        )
        user = User.objects.get(email=TEST_USER_EMAIL2)
        teacher = Teacher.objects.create(user=user)
                                 
        # Create our Student.
        User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        ).save()
        user = User.objects.get(email=TEST_USER_EMAIL)
        teacher = Teacher.objects.create(user=user)
                                 
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
    
    def get_logged_in_trudy_client(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME2,
            password=TEST_USER_PASSWORD2
        )
        return client
    
    def test_url_resolves_to_lectures_page_view(self):
        found = resolve('/teacher/course/1/lectures')
        self.assertEqual(found.func, lecture.lectures_page)
    
    def test_lectures_page_with_submission(self):
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/lectures')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'Lectures',response.content)

    def test_url_resolves_to_lecture_modal(self):
        found = resolve('/teacher/course/1/lecture_modal')
        self.assertEqual(found.func, lecture.lecture_modal)

    def test_lecture_modal_with_submission(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/lecture_modal',{
            'lecture_id': 1,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'lecture_modal',response.content)
        self.assertIn(b'Blade vs Evil',response.content)

    def test_lecture_modal_without_submission(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/lecture_modal',{
            'lecture_id': 0,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'lecture_modal',response.content)

    def test_save_lecture_with_insert(self):
        try:
            Lecture.objects.get(lecture_id=1).delete()
        except Lecture.DoesNotExist:
            pass
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/save_lecture',{
            'lecture_id': 0,
            'title': 'Blade vs Evil',
            'week_num': 1,
            'lecture_num': 1,
            'description': 'Video of a fight',
            'youtube_url': '',
            'preferred_service': settings.YOUTUBE_VIDEO_PLAYER,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')

    def test_save_lecture_with_update(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/save_lecture',{
            'lecture_id': 1,
            'title': 'Blade vs Evil',
            'week_num': 1,
            'lecture_num': 1,
            'description': 'Video of a fight',
            'youtube_url': '',
            'preferred_service': settings.YOUTUBE_VIDEO_PLAYER,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')

    def test_delete_lecture_with_empty_records(self):
        try:
            Lecture.objects.get(lecture_id=1).delete()
        except Lecture.DoesNotExist:
            pass
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/delete_lecture',{
            'lecture_id': 666,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'record not found')
        self.assertEqual(array['status'], 'failed')

    def test_delete_lecture_with_correct_user(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/delete_lecture',{
            'lecture_id': 1,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'deleted')
        self.assertEqual(array['status'], 'success')

    def test_delete_lecture_with_incorrect_user(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_trudy_client()
        response = client.post('/teacher/course/1/delete_lecture',{
            'lecture_id': 1,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'unauthorized deletion')
        self.assertEqual(array['status'], 'failed')
