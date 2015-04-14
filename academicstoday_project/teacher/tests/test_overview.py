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
TEST_USER_PASSWORD = "ContinentalUnion"
TEST_USER_EMAIL2 = "whalesquid@hideauze.com"
TEST_USER_USERNAME2 = "whalesquid"
TEST_USER_PASSWORD2 = "Evolvers"

class OverviewTestCase(TestCase):
    def tearDown(self):
        syllabuses = Syllabus.objects.all()
        for syllabus in syllabuses:
            syllabus.delete()
        policies = Policy.objects.all()
        for policy in policies:
            policy.delete()
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
                                 
        # Create our Teacher.
        user = User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        teacher = Teacher.objects.create(user=user)
        course = Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
            teacher=teacher,
        )

    def populate_course_content(self, client, kwargs):
        course = Course.objects.get(id=1)
        Announcement.objects.create(
            announcement_id=1,
            course=course,
            title='Hello world!',
            body='This is the body of the message.',
        )
        course = Course.objects.get(id=1)
        file_path = settings.MEDIA_ROOT + '/sample.pdf'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            Syllabus.objects.create(
                syllabus_id=1,
                file='',
                course=course,
            )
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            Policy.objects.create(
                policy_id=1,
                file='',
                course=course,
            )
            
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

    def delete_course_content(self):
        for id in range(1, 10):
            # Syllabus
            try:
                Syllabus.objects.get(syllabus_id=id).delete()
            except Syllabus.DoesNotExist:
                pass
            # Policy
            try:
                Policy.objects.get(policy_id=id).delete()
            except Policy.DoesNotExist:
                pass
        
        # Announcement
        try:
            Announcement.objects.get(announcement_id=1).delete()
        except Announcement.DoesNotExist:
            pass


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
        client = self.get_logged_in_client()
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        
        # Create course content.
        self.populate_course_content(client, kwargs)
        
        response = client.post('/teacher/course/1/submit_course_for_review',{}, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'submitted course review')
        self.assertEqual(array['status'], 'success')

        # Delete course content.
        self.delete_course_content()
