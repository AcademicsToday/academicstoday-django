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
from registrar.models import Lecture
from registrar.models import FileUpload
from teacher.views import lecture_note


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "ContinentalUnion"
TEST_USER_EMAIL2 = "whalesquid@hideauze.com"
TEST_USER_USERNAME2 = "whalesquid"
TEST_USER_PASSWORD2 = "Evolvers"


class LectureNoteTestCase(TestCase):
    def tearDown(self):
        courses = Course.objects.all()
        for course in courses:
            course.delete()
        uploads = FileUpload.objects.all()
        for upload in uploads:
            upload.delete()
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
    
    def test_url_resolves_to_lecture_notes_page_view(self):
        found = resolve('/teacher/course/1/lecture/1/notes')
        self.assertEqual(found.func, lecture_note.lecture_notes_page)
    
    def test_lecture_notes_page(self):
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/lecture/1/notes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'Lectures',response.content)

    def test_url_resolves_to_lecture_note_modal(self):
        found = resolve('/teacher/course/1/lecture/1/lecture_note_modal')
        self.assertEqual(found.func, lecture_note.lecture_note_modal)

    def test_lecture_modal(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/lecture/1/lecture_note_modal',{
            'upload_id': 0,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'lecture_modal',response.content)

    def test_save_lecture_note_with_no_record(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        file_path = settings.MEDIA_ROOT + '/sample.pdf'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/teacher/course/1/lecture/1/save_lecture_note',{
                'upload_id': 666,
                'title': 'Blade vs Evil',
                'description': 'Video of a fight',
                'file': fp,
            }, **kwargs)
            self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'record does not exist')
        self.assertEqual(array['status'], 'failed')

    def test_save_lecture_note_with_insert(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        file_path = settings.MEDIA_ROOT + '/sample.pdf'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/teacher/course/1/lecture/1/save_lecture_note',{
                'upload_id': 0,
                'title': 'Blade vs Evil',
                'description': 'Video of a fight',
                'file': fp,
            }, **kwargs)
            self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')

    def test_save_lecture_with_update(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        file_path = settings.MEDIA_ROOT + '/sample.pdf'
        
        # Insert
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/teacher/course/1/lecture/1/save_lecture_note',{
                'upload_id': 0,
                'title': 'Blade vs Evil',
                'description': 'Video of a fight',
                'file': fp,
            }, **kwargs)
            self.assertEqual(response.status_code, 200)
        
        # Update
        uploads = FileUpload.objects.all()  # Find uploaded file & use it's ID.
        upload = list(uploads).pop()
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/teacher/course/1/lecture/1/save_lecture_note',{
                'upload_id': upload.upload_id,
                'title': 'Blade vs Evil',
                'description': 'Video of a fight',
                'file': fp,
            }, **kwargs)
            self.assertEqual(response.status_code, 200)

    def test_delete_lecture_note_with_empty_records(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/lecture/1/delete_lecture_note',{
            'upload_id': 666,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'record not found')
        self.assertEqual(array['status'], 'failed')

    def test_delete_lecture_note_with_correct_user(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        file_path = settings.MEDIA_ROOT + '/sample.pdf'
        
        # Insert
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/teacher/course/1/lecture/1/save_lecture_note',{
                'upload_id': 0,
                'title': 'Blade vs Evil',
                'description': 'Video of a fight',
                'file': fp,
            }, **kwargs)
            self.assertEqual(response.status_code, 200)
        
        # Delete
        uploads = FileUpload.objects.all()  # Find uploaded file & use it's ID.
        upload = list(uploads).pop()
        response = client.post('/teacher/course/1/lecture/1/delete_lecture_note',{
            'upload_id': upload.upload_id,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'deleted')
        self.assertEqual(array['status'], 'success')

    def test_delete_lecture_note_with_incorrect_user(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        file_path = settings.MEDIA_ROOT + '/sample.pdf'
        
        # Insert
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/teacher/course/1/lecture/1/save_lecture_note',{
                'upload_id': 0,
                'title': 'Blade vs Evil',
                'description': 'Video of a fight',
                'file': fp,
            }, **kwargs)
            self.assertEqual(response.status_code, 200)
    
        # Delete
        uploads = FileUpload.objects.all()  # Find uploaded file & use it's ID.
        upload = list(uploads).pop()
        client.logout()
        client = self.get_logged_in_trudy_client()
        response = client.post('/teacher/course/1/lecture/1/delete_lecture_note',{
            'upload_id': upload.upload_id,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'unauthorized deletion')
        self.assertEqual(array['status'], 'failed')
