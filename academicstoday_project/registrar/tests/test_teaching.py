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
from registrar.views import teaching


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"
TEST_USER_EMAIL2 = "whalesquid@hideauze.com"
TEST_USER_USERNAME2 = "whalesquid"
TEST_USER_PASSWORD2 = "passwordabc"


class TeachingTestCase(TestCase):
    def tearDown(self):
        courses = Course.objects.all()
        for course in courses:
            course.delete()
        User.objects.all().delete()

    def setUp(self):
        # Create our user.
        User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user = User.objects.get(email=TEST_USER_EMAIL)
        teacher = Teacher.objects.create(user=user)
    
    def test_url_resolves_to_teaching_page_view(self):
        found = resolve('/teaching')
        self.assertEqual(found.func, teaching.teaching_page)
    
    def test_teacher_page(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/teaching')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Teaching',response.content)
        self.assertIn(b'ajax_table_placeholder',response.content)

    def test_url_resolves_to_teaching_table(self):
        found = resolve('/refresh_teaching_table')
        self.assertEqual(found.func, teaching.refresh_teaching_table)

    def test_refresh_teaching_table_with_course(self):
        user = User.objects.get(email=TEST_USER_EMAIL)
        teacher = Teacher.objects.get(user=user)
        Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
            teacher=teacher,
        )
        
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/refresh_teaching_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'view_course_page(1);',response.content)
        self.assertIn(b'ajax_delete_course_modal(1);',response.content)

    def test_url_resolves_to_new_course_modal(self):
        found = resolve('/course_modal')
        self.assertEqual(found.func, teaching.course_modal)

    def test_course_modal(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/course_modal',{
            'course_id':0,
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ajax_create_course();',response.content)

    def test_url_resolves_to_save_course_json(self):
        found = resolve('/save_course')
        self.assertEqual(found.func, teaching.save_course)
    
    def test_save_new_course(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        file_path = settings.MEDIA_ROOT + '/sample.png'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/save_course', {
                'course_id': 0,
                'finish_date': '2040-01-01',
                'category': 'Electrical Engineering',
                'start_date': '2015-01-01',
                'title': 'Cybernetics',
                'sub_title': 'We asked for this.',
                'image': fp,
                'description': 'HOWTO Guide on upgrading yourself.',
            }, **kwargs)
            self.assertEqual(response.status_code, 200)
            json_string = response.content.decode(encoding='UTF-8')
            array = json.loads(json_string)
            self.assertEqual(array['message'], 'course saved')
            self.assertEqual(array['status'], 'success')

    def test_url_resolves_to_delete_course_modal(self):
        found = resolve('/delete_course_modal')
        self.assertEqual(found.func, teaching.delete_course_modal)
    
    def test_delete_course_modal(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/delete_course_modal')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ajax_delete_course();',response.content)


    def test_url_resolves_to_course_delete(self):
        found = resolve('/course_delete')
        self.assertEqual(found.func, teaching.course_delete)
    
    def test_course_delete_with_correct_user(self):
        user = User.objects.get(email=TEST_USER_EMAIL)
        teacher = Teacher.objects.get(user=user)
        Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
            teacher=teacher,
        )
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = client.post('/course_delete', {
                       'course_id': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'deleted')
        self.assertEqual(array['status'], 'success')

    def test_course_delete_with_wrong_user(self):
        # Create our user & course
        User.objects.create_user(
            email=TEST_USER_EMAIL2,
            username=TEST_USER_USERNAME2,
            password=TEST_USER_PASSWORD2
        )
        user = User.objects.get(email=TEST_USER_EMAIL2)
        teacher = Teacher.objects.create(user=user)
        Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
            teacher=teacher,
        )
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = client.post('/course_delete', {
            'course_id': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'unauthorized deletion')
        self.assertEqual(array['status'], 'failed')
