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
from registrar.models import Course
from registrar.models import Student
from registrar.models import Teacher
from registrar.models import CourseDiscussionPost
from registrar.models import CourseDiscussionThread
from student.views import discussion


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"
TEST_USER_EMAIL2 = "whalesquid@hideauze.com"
TEST_USER_USERNAME2 = "whalesquid"
TEST_USER_PASSWORD2 = "passwordabc"


class DiscussionTestCase(TestCase):
    def tearDown(self):
        courses = Course.objects.all()
        for course in courses:
            course.delete()
        User.objects.all().delete()

    def setUp(self):
        # Create our Trudy student
        User.objects.create_user(
            email=TEST_USER_EMAIL2,
            username=TEST_USER_USERNAME2,
            password=TEST_USER_PASSWORD2
        )
        user = User.objects.get(email=TEST_USER_EMAIL2)
        teacher = Teacher.objects.create(user=user)
        Student.objects.create(user=user).save()
                                 
        # Create our user.
        User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user = User.objects.get(email=TEST_USER_EMAIL)
        teacher = Teacher.objects.create(user=user)

        # Create a test course
        Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
            teacher=teacher,
        )
    
        course = Course.objects.get(id=1)
        user = User.objects.get(email=TEST_USER_EMAIL)
        CourseDiscussionThread.objects.create(
            thread_id=1,
            title="Glory...",
            text="Glory to the Galactic Alliance of Humankind!",
            user=user,
            course=course,
        )
        CourseDiscussionPost.objects.create(
            post_id=1,
            user=user,
            title='Hideazue...',
            text='We will spread the domain of the living throughout the universe!'
        )
        thread = CourseDiscussionThread.objects.get(thread_id=1)
        post = CourseDiscussionPost.objects.get(post_id=1)
        thread.posts.add(post)

    def get_logged_in_client(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        return client

    def test_url_resolves_to_discussion_page_view(self):
        found = resolve('/course/1/discussion')
        self.assertEqual(found.func, discussion.discussion_page)

    def test_discussion_page_without_thread(self):
        CourseDiscussionThread.objects.get(
            thread_id=1
        ).delete()
        client = self.get_logged_in_client()
        response = client.post('/course/1/discussion')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)

    def test_discussion_page_with_thread(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/discussion')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'Glory...',response.content)
    
    def test_threads_table_without_thread(self):
        CourseDiscussionThread.objects.get(
            thread_id=1
        ).delete()
        client = self.get_logged_in_client()
        response = client.post('/course/1/threads_table')
        self.assertEqual(response.status_code, 200)
    
    def test_threads_table_with_thread(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/threads_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Glory...',response.content)

    def test_new_thread_modal(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/new_thread')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'new_thread_modal',response.content)

    def test_insert_thread(self):
        CourseDiscussionThread.objects.get(
            thread_id=1
        ).delete()
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/course/1/insert_thread',{
            'title': 'Hideazue...',
            'text': 'We will spread the domain of the living throughout the universe!'
        }, **kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['message'], 'submitted')
        self.assertEqual(array['status'], 'success')

    def test_delete_thread_with_correct_user(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/course/1/delete_thread',{
            'thread_id': 1,
        }, **kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'thread was deleted')
    
    def test_delete_thread_with_incorrect_user(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        client.logout()
        client.login(
            username=TEST_USER_USERNAME2,
            password=TEST_USER_PASSWORD2
        )
        response = client.post('/course/1/delete_thread',{
            'thread_id': 1,
        }, **kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'failed')
        self.assertEqual(array['message'], 'unauthorized deletion')


    def test_url_resolves_to_thread_page_view(self):
        found = resolve('/course/1/thread/1')
        self.assertEqual(found.func, discussion.thread_page)
    
    def test_thread_page(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/thread/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'Hideazue...',response.content)

    def test_post_table(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/thread/1/posts_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hideazue...',response.content)

    def test_new_post_modal(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/thread/1/new_post')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'new_post_modal',response.content)

    def test_insert_post(self):
        CourseDiscussionPost.objects.get(
            post_id=1
        ).delete()
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/course/1/thread/1/insert_post',{
            'title': 'Hideazue...',
            'text': 'We will spread the domain of the living throughout the universe!'
        }, **kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['message'], 'submitted')
        self.assertEqual(array['status'], 'success')