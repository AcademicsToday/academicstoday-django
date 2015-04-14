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
from registrar.models import Quiz
from registrar.models import QuizSubmission
from registrar.models import TrueFalseQuestion
from registrar.models import TrueFalseSubmission
from teacher.views import quiz


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "ContinentalUnion"
TEST_USER_EMAIL2 = "whalesquid@hideauze.com"
TEST_USER_USERNAME2 = "whalesquid"
TEST_USER_PASSWORD2 = "Evolvers"


class QuizTestCase(TestCase):
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
        ).save()
    
        course = Course.objects.get(id=1)
        Quiz.objects.create(
            quiz_id=1,
            quiz_num=1,
            title="Hideauze",
            description="Anime related assignment.",
            worth=25,
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

    def test_url_resolves_to_quizzes_page_view(self):
        found = resolve('/teacher/course/1/quizzes')
        self.assertEqual(found.func, quiz.quizzes_page)

    def test_quizzes_page_with_no_submissions(self):
        try:
            Quiz.objects.get(quiz_id=1).delete()
        except Quiz.DoesNotExist:
            pass
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/quizzes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'ajax_quiz_modal',response.content)

    def test_url_resolves_to_quiz_table_view(self):
        found = resolve('/teacher/course/1/quizzes_table')
        self.assertEqual(found.func, quiz.quizzes_table)

    def test_quizzes_table_returns_with_no_submissions(self):
        try:
            Quiz.objects.get(quiz_id=1).delete()
        except Quiz.DoesNotExist:
            pass
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/quizzes_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ajax_quiz(0);',response.content)

    def test_quizzes_table_returns_with_submissions(self):
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/quizzes_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ajax_quiz(1);',response.content)

    def test_url_resolves_to_delete_quiz(self):
        found = resolve('/teacher/course/1/delete_quiz')
        self.assertEqual(found.func, quiz.delete_quiz)
    
    def test_delete_quiz_with_no_submissions(self):
        try:
            Quiz.objects.get(quiz_id=1).delete()
        except Quiz.DoesNotExist:
            pass
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/delete_quiz',{
            'quiz_id': 1,
        }, **kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['status'], 'failed')
        self.assertEqual(array['message'], 'record does not exist')

    def test_delete_quiz_with_submissions(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/delete_quiz',{
            'quiz_id': 1,
        }, **kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'deleted')

    def test_delete_quiz_with_submissions(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_trudy_client()
        response = client.post('/teacher/course/1/delete_quiz',{
            'quiz_id': 1,
        }, **kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'deleted')

    def test_url_resolves_to_save_quiz(self):
        found = resolve('/teacher/course/1/save_quiz')
        self.assertEqual(found.func, quiz.save_quiz)
    
    def test_save_quiz_with_insert(self):
        try:
            Quiz.objects.get(quiz_id=1).delete()
        except Quiz.DoesNotExist:
            pass
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/save_quiz',{
            'quiz_id': 0,
            'quiz_num': 1,
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

    def test_save_quiz_with_update(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/save_quiz',{
            'quiz_id': 1,
            'quiz_num': 1,
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

    def test_url_resolves_to_quiz_page_view(self):
        found = resolve('/teacher/course/1/quiz/1')
        self.assertEqual(found.func, quiz.quiz_page)

    def test_quiz_page(self):
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/quiz/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ajax_question_modal',response.content)

    def test_save_question_with_insert_true_false_question(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/quiz/1/save_question',{
            'question_id': 0,
            'question_type': settings.TRUEFALSE_QUESTION_TYPE,
            'question_num': 3,
            'title': 'Hideauze',
            'description': 'Where the Hideauze once humans?',
            'true_choice':'Yes, former humans',
            'false_choice':'No, aliens',
            'answer': True,
            'marks': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'question was saved')
        self.assertEqual(array['status'], 'success')

    def test_save_question_with_update_true_false_question(self):
        # Insert
        TrueFalseQuestion.objects.create(
            question_id=3,
            quiz=Quiz.objects.get(quiz_id=1),
            title="Hideauze",
            description="Where the Hideauze human?",
            true_choice="Yes, former humans",
            false_choice="No, aliens",
            answer=True,
        )
        
        # Update
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/quiz/1/save_question',{
            'question_id': 3,
            'question_type': settings.TRUEFALSE_QUESTION_TYPE,
            'question_num': 3,
            'title': 'Hideauze',
            'description': 'Where the Hideauze once humans?',
            'true_choice':'Yes, former humans',
            'false_choice':'No, aliens',
            'answer': True,
            'marks': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'question was saved')
        self.assertEqual(array['status'], 'success')

    def test_delete_question_with_true_false_question(self):
        TrueFalseQuestion.objects.create(
            question_id=3,
            quiz=Quiz.objects.get(quiz_id=1),
            title="Hideauze",
            description="Where the Hideauze human?",
            true_choice="Yes, former humans",
            false_choice="No, aliens",
            answer=True,
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/quiz/1/delete_question',{
            'question_id': 3,
            'question_type': settings.TRUEFALSE_QUESTION_TYPE,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'question was deleted')
        self.assertEqual(array['status'], 'success')

    def test_url_resolves_to_questions_table_view(self):
        found = resolve('/teacher/course/1/quiz/1/questions_table')
        self.assertEqual(found.func, quiz.questions_table)

    def test_questions_table_returns_without_questions(self):
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/quiz/1/questions_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ajax_question(0,0);',response.content)

    def test_questions_table_returns_with_questions(self):
        TrueFalseQuestion.objects.create(
            question_id=4,
            quiz=Quiz.objects.get(quiz_id=1),
        )
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/quiz/1/questions_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ajax_delete_question(',response.content)

    def test_question_type_modal(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/quiz/1/question_type_modal',**kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'question_modal',response.content)

    def test_question_true_false_modal(self):
        TrueFalseQuestion.objects.create(
                question_id=3,
                quiz=Quiz.objects.get(quiz_id=1),
            title="Hideauze",
            description="Where the Hideauze human?",
            true_choice="Yes, former humans",
            false_choice="No, aliens",
            answer=True,
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/quiz/1/question_true_false_modal',{
            'question_id':3,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'question_modal',response.content)
