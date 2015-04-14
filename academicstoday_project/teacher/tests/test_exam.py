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
from registrar.models import Exam
from registrar.models import ExamSubmission
from registrar.models import MultipleChoiceQuestion
from registrar.models import MultipleChoiceSubmission


# View
from teacher.views import exam

# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "ContinentalUnion"
TEST_USER_EMAIL2 = "whalesquid@hideauze.com"
TEST_USER_USERNAME2 = "whalesquid"
TEST_USER_PASSWORD2 = "Evolvers"

class ExamTestCase(TestCase):
    def tearDown(self):
        User.objects.get(email=TEST_USER_EMAIL).delete()
        courses = Course.objects.all()
        for course in courses:
            course.delete()

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
        ).save()
    
        course = Course.objects.get(id=1)
        Exam.objects.create(
            exam_id=1,
            exam_num=1,
            title="Hideauze",
            description="Anime related assignment.",
            worth=25,
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

    def get_logged_in_trudy_client(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME2,
            password=TEST_USER_PASSWORD2
        )
        return client

    def test_url_resolves_to_exams_page_view(self):
        found = resolve('/teacher/course/1/exams')
        self.assertEqual(found.func, exam.exams_page)

    def test_exams_page_with_no_submissions(self):
        try:
            Exam.objects.get(exam_id=1).delete()
        except Exam.DoesNotExist:
            pass
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/exams')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'ajax_exam_table',response.content)

    def test_url_resolves_to_exams_table_view(self):
        found = resolve('/teacher/course/1/exams_table')
        self.assertEqual(found.func, exam.exams_table)

    def test_exams_table_with_no_submissions(self):
        try:
            Exam.objects.get(exam_id=1).delete()
        except Exam.DoesNotExist:
            pass
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/exams_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ajax_exam(0);',response.content)

    def test_exams_table_with_submissions(self):
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/exams_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ajax_exam(1);',response.content)

    def test_url_resolves_to_delete_exam(self):
        found = resolve('/teacher/course/1/delete_exam')
        self.assertEqual(found.func, exam.delete_exam)
    
    def test_delete_exam_without_submissions(self):
        try:
            Exam.objects.get(exam_id=1).delete()
        except Exam.DoesNotExist:
            pass
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/delete_exam',{
            'exam_id': 1,
        }, **kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['status'], 'failed')
        self.assertEqual(array['message'], 'record does not exist')

    def test_delete_exam_with_submissions_and_correct_user(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/delete_exam',{
            'exam_id': 1,
        }, **kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'deleted')

    def test_delete_exam_with_submissions_and_incorrect_user(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_trudy_client()
        response = client.post('/teacher/course/1/delete_exam',{
            'exam_id': 1,
        }, **kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['status'], 'failed')
        self.assertEqual(array['message'], 'unauthorized deletion')

    def test_url_resolves_to_save_exam(self):
        found = resolve('/teacher/course/1/save_exam')
        self.assertEqual(found.func, exam.save_exam)
    
    def test_save_exam_with_insert(self):
        try:
            Exam.objects.get(exam_id=1).delete()
        except Exam.DoesNotExist:
            pass
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/save_exam',{
            'exam_id': 0,
            'exam_num': 1,
            'title': 'Test',
            'description': 'Test',
            'start_date': '2020-01-01',
            'due_date': '2020-01-01',
            'worth': 25,
        }, **kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')

    def test_save_exam_with_update(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/save_exam',{
            'exam_id': 1,
            'exam_num': 1,
            'title': 'Test',
            'description': 'Test',
            'start_date': '2020-01-01',
            'due_date': '2020-01-01',
            'worth': 25,
        }, **kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['message'], 'saved')
        self.assertEqual(array['status'], 'success')

    def test_url_resolves_to_exam_page_view(self):
        found = resolve('/teacher/course/1/exam/1')
        self.assertEqual(found.func, exam.exam_page)

    def test_exam_page(self):
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/exam/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ajax_question_modal',response.content)

    def test_save_question_with_insert_multiple_choice_question(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/exam/1/save_question',{
            'question_id': 0,
            'question_type': settings.MULTIPLECHOICE_QUESTION_TYPE,
            'question_num': 1,
            'title': 'Sun',
            'description': 'Why did humanity leave Earth?',
            'a': 'Global Cooling',
            'b': 'Abnormal Solar Hibernation',
            'c': 'Global Warming',
            'd': 'World Peace',
            'a_is_correct': True,
            'b_is_correct': True,
            'marks': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'question was saved')
        self.assertEqual(array['status'], 'success')

    def test_save_question_with_update_multiple_choice_question(self):
        # Insert
        MultipleChoiceQuestion.objects.create(
            question_id=2,
            exam=Exam.objects.get(exam_id=1),
            title="Hideauze",
            description="Who where the Hideauze?",
            a="Former Humans",
            a_is_correct=True,
            b="Aliens",
            b_is_correct=False,
            c="Magical or Supernatural Creatures",
            c_is_correct=False,
            d="Transhumanists",
            d_is_correct=True,
            e="Heavenly Creatures",
            e_is_correct=True,
        )
        
        # Update
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/exam/1/save_question',{
            'question_id': 2,
            'question_type': settings.MULTIPLECHOICE_QUESTION_TYPE,
            'question_num': 1,
            'title': 'Sun',
            'description': 'Why did humanity leave Earth?',
            'a': 'Global Cooling',
            'b': 'Abnormal Solar Hibernation',
            'c': 'Global Warming',
            'd': 'World Peace',
            'a_is_correct': True,
            'b_is_correct': True,
            'marks': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'question was saved')
        self.assertEqual(array['status'], 'success')

    def test_delete_question_with_multiple_choice_question_and_correct_user(self):
        MultipleChoiceQuestion.objects.create(
            question_id=2,
            exam=Exam.objects.get(exam_id=1),
            title="Hideauze",
            description="Who where the Hideauze?",
            a="Former Humans",
            a_is_correct=True,
            b="Aliens",
            b_is_correct=False,
            c="Magical or Supernatural Creatures",
            c_is_correct=False,
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/exam/1/delete_question',{
            'question_id': 2,
            'question_type': settings.MULTIPLECHOICE_QUESTION_TYPE,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'question was deleted')
        self.assertEqual(array['status'], 'success')
    
    def test_delete_question_with_multiple_choice_question_and_incorrect_user(self):
        MultipleChoiceQuestion.objects.create(
            question_id=2,
            exam=Exam.objects.get(exam_id=1),
            title="Hideauze",
            description="Who where the Hideauze?",
            a="Former Humans",
            a_is_correct=True,
            b="Aliens",
            b_is_correct=False,
            c="Magical or Supernatural Creatures",
            c_is_correct=False,
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_trudy_client()
        response = client.post('/teacher/course/1/exam/1/delete_question',{
            'question_id': 2,
            'question_type': settings.MULTIPLECHOICE_QUESTION_TYPE,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'unauthorized deletion')
        self.assertEqual(array['status'], 'failed')

    def test_url_resolves_to_questions_table_view(self):
        found = resolve('/teacher/course/1/exam/1/questions_table')
        self.assertEqual(found.func, exam.questions_table)
    
    def test_questions_table_returns_without_questions(self):
        exam = Exam.objects.get(exam_id=1)
        try:
            MultipleChoiceQuestion.objects.get(exam_id=1).delete()
        except MultipleChoiceQuestion.DoesNotExist:
            pass
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/exam/1/questions_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ajax_question(0,0);',response.content)

    def test_questions_table_returns_with_questions(self):
        MultipleChoiceQuestion.objects.create(
            question_id=2,
            exam=Exam.objects.get(exam_id=1)
        )
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/exam/1/questions_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Multiple Choice',response.content)

    def test_question_type_modal(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/exam/1/question_type_modal',**kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'question_modal',response.content)

    def test_question_multiple_choice_modal(self):
        MultipleChoiceQuestion.objects.create(
            question_id=2,
            exam=Exam.objects.get(exam_id=1),
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/exam/1/question_multiple_choice_modal',{
            'question_id':2,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'question_modal',response.content)
