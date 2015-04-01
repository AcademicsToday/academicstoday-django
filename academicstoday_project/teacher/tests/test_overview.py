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
from registrar.models import Teacher
from registrar.models import Course
from registrar.models import Announcement
from registrar.models import Syllabus
from registrar.models import Policy
from registrar.models import Lecture
from registrar.models import Assignment
from registrar.models import Quiz
from registrar.models import Exam
from registrar.models import CourseSubmission

# View
from teacher.views import overview

# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"

class OverviewTestCase(TestCase):
    def tearDown(self):
        # User
        try:
            User.objects.get(email=TEST_USER_EMAIL).delete()
        except User.DoesNotExist:
            pass
        # Syllabus
        try:
            Syllabus.objects.get(syllabus_id=1).delete()
        except Syllabus.DoesNotExist:
            pass
        try:
            Syllabus.objects.get(syllabus_id=2).delete()
        except Syllabus.DoesNotExist:
            pass
        try:
            Syllabus.objects.get(syllabus_id=3).delete()
        except Syllabus.DoesNotExist:
            pass
        # Policy
        try:
            Policy.objects.get(policy_id=1).delete()
        except Policy.DoesNotExist:
            pass
        try:
            Policy.objects.get(policy_id=2).delete()
        except Policy.DoesNotExist:
            pass
        try:
            Policy.objects.get(policy_id=3).delete()
        except Policy.DoesNotExist:
            pass
        # Announcement
        try:
            Announcement.objects.get(announcement_id=1).delete()
        except Announcement.DoesNotExist:
            pass

    def setUp(self):
        user = User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        teacher = Teacher.objects.create(user=user)
        
        # Course
        course = Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
        )
        
        # Announcement
        Announcement.objects.create(
            announcement_id=1,
            course=course,
            title='Hello world!',
            body='This is the body of the message.',
        )
        
        # Syllabus + Policy Upload
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        file_path = settings.MEDIA_ROOT + '/sample.pdf'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            client.post('/teacher/course/1/save_syllabus',{
                'file': fp,
            }, **kwargs)
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            client.post('/teacher/course/1/save_policy',{
                'file': fp,
            }, **kwargs)
        
        # Lectures
        Lecture.objects.create(
            lecture_id=1,
            lecture_num=1,
            week_num=1,
            title="Blade vs Evil",
            description="Fighting for the destiny of the Earth.",
            course=course,
        )

        Lecture.objects.create(
            lecture_id=2,
            lecture_num=2,
            week_num=1,
            title="Blade vs Evil",
            description="Fighting for the destiny of the Earth.",
            course=course,
        )

        # Assignments
        Assignment.objects.create(
            assignment_id=1,
            assignment_num=1,
            title="Hideauze",
            description="Anime related assignment.",
            worth=25,
            course=course,
        )
        Quiz.objects.create(
            quiz_id=1,
            quiz_num=1,
            title="Hideauze",
            description="Anime related assignment.",
            worth=25,
            course=course,
        )
        Exam.objects.create(
            exam_id=1,
            exam_num=1,
            title="Hideauze",
            description="Anime related assignment.",
            worth=50,
            course=course,
            is_final=True,
        )
            
    
    def get_logged_in_client(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        return client

    def test_url_resolves_to_overview_page_view(self):
        found = resolve('/teacher/course/1/overview')
        self.assertEqual(found.func, overview.overview_page)

    def test_overview_page(self):
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/overview')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'ajax_submit_course()',response.content)

    def test_submit_course_for_review(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/submit_course_for_review',{}, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'submitted course review')
        self.assertEqual(array['status'], 'success')