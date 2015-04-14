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
from registrar.models import Exam
from registrar.models import ExamSubmission
from registrar.models import MultipleChoiceQuestion
from registrar.models import MultipleChoiceSubmission
from student.views import exam


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "ContinentalUnion"
TEST_USER_EMAIL2 = "whalesquid@hideauze.com"
TEST_USER_USERNAME2 = "whalesquid"
TEST_USER_PASSWORD2 = "Evolvers"


class ExamTestCase(TestCase):
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

        # Create our assignment(s)
        Exam.objects.create(
            exam_id=1,
            exam_num=1,
            title="Hideauze",
            description="Anime related assignment.",
            worth=50,
            course=course,
        )
        exam = Exam.objects.get(exam_id=1)

        # Create questions
        MultipleChoiceQuestion.objects.create(
            question_id=2,
            exam=exam,
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
    
    def get_logged_in_client(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        return client

    def test_url_resolves_to_exams_page_view(self):
        found = resolve('/course/1/exams')
        self.assertEqual(found.func, exam.exams_page)

    def test_exams_page_with_no_submissions(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/exams')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'view_exam(1);',response.content)

    def test_url_resolves_to_exams_table_view(self):
        found = resolve('/course/1/exams_table')
        self.assertEqual(found.func, exam.exams_table)

    def test_exams_table_returns_with_no_submissions(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/exams_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'view_exam(1);',response.content)
    
    def test_url_resolves_to_delete_exam(self):
        found = resolve('/course/1/delete_exam')
        self.assertEqual(found.func, exam.delete_exam)
    
    def test_delete_exam_with_no_submissions(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/course/1/delete_exam',{
            'exam_id': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'failed')
        self.assertEqual(array['message'], 'record does not exist')
    
    def test_delete_exam_with_submissions_and_correct_user(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/course/1/exam/1/submit_exam',{}, **kwargs)
        self.assertEqual(response.status_code, 200)
        response = client.post('/course/1/delete_exam',{
            'exam_id': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'exam was deleted')
    
    def test_delete_exam_with_submissions_and_incorrect_user(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/course/1/exam/1/submit_exam',{}, **kwargs)
        self.assertEqual(response.status_code, 200)
        client.logout()
        client.login(
            username=TEST_USER_USERNAME2,
            password=TEST_USER_PASSWORD2
        )
        response = client.post('/course/1/delete_exam',{
            'exam_id': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'failed')
        self.assertEqual(array['message'], 'record does not exist')

    def test_url_resolves_to_exam_page_view(self):
        found = resolve('/course/1/exam/1')
        self.assertEqual(found.func, exam.exam_page)

    def test_assignment_page(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/exam/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Exam #1',response.content)

    def test_submit_mc_exam_answer_with_submissions(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/course/1/exam/1/submit_mc_exam_answer',{
            'question_id': 2,
            'answer': 'A',
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'submitted')

    def test_submit_exam_without_answering_questions(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/course/1/exam/1/submit_exam',{}, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'submitted')
        self.assertEqual(array['status'], 'success')
    
    def test_submit_quiz_with_answering_questions(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        client.post('/course/1/exam/1/submit_tf_exam_answer',{
            'question_id': 1,
            'answer': 'A',
        }, **kwargs)
        response = client.post('/course/1/exam/1/submit_exam',{}, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'submitted')
        self.assertEqual(array['status'], 'success')