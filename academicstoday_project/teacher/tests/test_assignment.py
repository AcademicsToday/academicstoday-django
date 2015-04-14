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
from registrar.models import Assignment
from registrar.models import AssignmentSubmission
from registrar.models import EssayQuestion
from registrar.models import EssaySubmission
from registrar.models import MultipleChoiceQuestion
from registrar.models import MultipleChoiceSubmission
from registrar.models import ResponseQuestion
from registrar.models import ResponseSubmission
from registrar.models import TrueFalseQuestion
from registrar.models import TrueFalseSubmission


# View
from teacher.views import assignment

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
class AssignmentTestCase(TestCase):
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
        Assignment.objects.create(
            assignment_id=1,
            assignment_num=1,
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

    def test_url_resolves_to_assignments_page_view(self):
        found = resolve('/teacher/course/1/assignments')
        self.assertEqual(found.func, assignment.assignments_page)

    def test_assignments_page_with_no_submissions(self):
        try:
            Assignment.objects.get(assignment_id=1).delete()
        except Assignment.DoesNotExist:
            pass
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/assignments')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'ajax_assignment_modal',response.content)

    def test_url_resolves_to_assignment_table_view(self):
        found = resolve('/teacher/course/1/assignments_table')
        self.assertEqual(found.func, assignment.assignments_table)

    def test_assignments_table_returns_with_no_submissions(self):
        try:
            Assignment.objects.get(assignment_id=1).delete()
        except Assignment.DoesNotExist:
            pass
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/assignments_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ajax_assignment(0);',response.content)

    def test_url_resolves_to_delete_assignment(self):
        found = resolve('/teacher/course/1/delete_assignment')
        self.assertEqual(found.func, assignment.delete_assignment)
    
    def test_delete_assignment_with_no_submissions(self):
        try:
            Assignment.objects.get(assignment_id=1).delete()
        except Assignment.DoesNotExist:
            pass
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/delete_assignment',{
            'assignment_id': 1,
        }, **kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['status'], 'failed')
        self.assertEqual(array['message'], 'record not found')

    def test_delete_assignment_with_submissions_and_correct_user(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/delete_assignment',{
            'assignment_id': 1,
        }, **kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'assignment was deleted')

    def test_delete_assignment_with_submissions_and_incorrect_user(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_trudy_client()
        response = client.post('/teacher/course/1/delete_assignment',{
            'assignment_id': 1,
        }, **kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['status'], 'failed')
        self.assertEqual(array['message'], 'unauthorized deletion')

    def test_url_resolves_to_save_assignment(self):
        found = resolve('/teacher/course/1/save_assignment')
        self.assertEqual(found.func, assignment.save_assignment)
    
    def test_save_assignment_with_insert(self):
        try:
            Assignment.objects.get(assignment_id=1).delete()
        except Assignment.DoesNotExist:
            pass
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/save_assignment',{
            'assignment_id': 0,
            'assignment_num': 1,
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

    def test_save_assignment_with_update(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/save_assignment',{
            'assignment_id': 1,
            'assignment_num': 1,
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

    def test_url_resolves_to_assignment_page_view(self):
        found = resolve('/teacher/course/1/assignment/1')
        self.assertEqual(found.func, assignment.assignment_page)

    def test_assignment_page(self):
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/assignment/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ajax_question_modal',response.content)

    def test_save_question_with_insert_essay_question(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/assignment/1/save_question',{
            'question_id': 0,
            'question_type': settings.ESSAY_QUESTION_TYPE,
            'question_num': 1,
            'title': 'H+',
            'description': 'What does it mean to be a human being?',
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'question was saved')
        self.assertEqual(array['status'], 'success')

    def test_save_question_with_update_essay_question(self):
        # Insert
        EssayQuestion.objects.create(
            question_id=1,
            assignment=Assignment.objects.get(assignment_id=1),
            title="Evolvers",
            description="Write an essay about the Evolvers.",
        )
        
        # Update
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/assignment/1/save_question',{
            'question_id': 1,
            'question_type': settings.ESSAY_QUESTION_TYPE,
            'question_num': 1,
            'title': 'H+',
            'description': 'What does it mean to be a human being?',
            'marks': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'question was saved')
        self.assertEqual(array['status'], 'success')

    def test_save_question_with_insert_multiple_choice_question(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/assignment/1/save_question',{
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
            assignment=Assignment.objects.get(assignment_id=1),
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
        response = client.post('/teacher/course/1/assignment/1/save_question',{
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

    def test_save_question_with_insert_true_false_question(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/assignment/1/save_question',{
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
            assignment=Assignment.objects.get(assignment_id=1),
            title="Hideauze",
            description="Where the Hideauze human?",
            true_choice="Yes, former humans",
            false_choice="No, aliens",
            answer=True,
        )
        
        # Update
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/assignment/1/save_question',{
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

    def test_save_question_with_insert_response_question(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/assignment/1/save_question',{
            'question_id': 0,
            'question_type': settings.RESPONSE_QUESTION_TYPE,
            'question_num': 4,
            'title': 'Ice Age',
            'description': 'Why did humanity migrate off-world?',
            'answer': 'Because of solar hibernation causing Global Cooling on Earth.',
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'question was saved')
        self.assertEqual(array['status'], 'success')

    def test_save_question_with_update_response_question(self):
        # Insert
        ResponseQuestion.objects.create(
            question_id=4,
            assignment=Assignment.objects.get(assignment_id=1),
            title="Ice Age",
            description="Why did humanity migrate off-world?",
            answer="Because of solar hibernation causing Global Cooling on Earth.",
        )
        
        # Update
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/assignment/1/save_question',{
            'question_id': 4,
            'question_type': settings.RESPONSE_QUESTION_TYPE,
            'question_num': 4,
            'title': 'Mecha',
            'description': 'What was the name of Ledos mech?',
            'answer': 'Chambers',
            'marks': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'question was saved')
        self.assertEqual(array['status'], 'success')

    def test_delete_question_with_essay_question(self):
        EssayQuestion.objects.create(
            question_id=1,
            assignment=Assignment.objects.get(assignment_id=1),
            title="Evolvers",
            description="Write an essay about the Evolvers.",
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/assignment/1/delete_question',{
            'question_id': 1,
            'question_type': settings.ESSAY_QUESTION_TYPE,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'question was deleted')
        self.assertEqual(array['status'], 'success')

    def test_delete_question_with_multiple_choice_question(self):
        MultipleChoiceQuestion.objects.create(
            question_id=2,
            assignment=Assignment.objects.get(assignment_id=1),
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
        response = client.post('/teacher/course/1/assignment/1/delete_question',{
            'question_id': 2,
            'question_type': settings.MULTIPLECHOICE_QUESTION_TYPE,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'question was deleted')
        self.assertEqual(array['status'], 'success')

    def test_delete_question_with_true_false_question(self):
        TrueFalseQuestion.objects.create(
            question_id=3,
            assignment=Assignment.objects.get(assignment_id=1),
            title="Hideauze",
            description="Where the Hideauze human?",
            true_choice="Yes, former humans",
            false_choice="No, aliens",
            answer=True,
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/assignment/1/delete_question',{
            'question_id': 3,
            'question_type': settings.TRUEFALSE_QUESTION_TYPE,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'question was deleted')
        self.assertEqual(array['status'], 'success')

    def test_delete_question_with_response_question(self):
        ResponseQuestion.objects.create(
            question_id=4,
            assignment=Assignment.objects.get(assignment_id=1),
            title="Ice Age",
            description="Why did humanity migrate off-world?",
            answer="Because of solar hibernation causing Global Cooling on Earth.",
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/assignment/1/delete_question',{
            'question_id': 4,
            'question_type': settings.RESPONSE_QUESTION_TYPE,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'question was deleted')
        self.assertEqual(array['status'], 'success')

    def test_url_resolves_to_questions_table_view(self):
        found = resolve('/teacher/course/1/assignment/1/questions_table')
        self.assertEqual(found.func, assignment.questions_table)
    
    def test_questions_table_returns_without_questions(self):
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/assignment/1/questions_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ajax_question(0,0);',response.content)

    def test_questions_table_returns_with_questions(self):
        ResponseQuestion.objects.create(
            question_id=4,
            assignment=Assignment.objects.get(assignment_id=1),
            title="Ice Age",
            description="Why did humanity migrate off-world?",
            answer="Because of solar hibernation causing Global Cooling on Earth.",
        )
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/assignment/1/questions_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Response',response.content)

    def test_question_type_modal(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/assignment/1/question_type_modal',**kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'question_modal',response.content)

    def test_question_essay_modal(self):
        EssayQuestion.objects.create(
            question_id=1,
            assignment=Assignment.objects.get(assignment_id=1),
            title="Evolvers",
            description="Write an essay about the Evolvers.",
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/assignment/1/question_essay_modal',{
            'question_id': 1,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'question_modal',response.content)

    def test_question_multiple_choice_modal(self):
        MultipleChoiceQuestion.objects.create(
            question_id=2,
            assignment=Assignment.objects.get(assignment_id=1),
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
        response = client.post('/teacher/course/1/assignment/1/question_multiple_choice_modal',{
            'question_id':2,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'question_modal',response.content)

    def test_question_true_false_modal(self):
        TrueFalseQuestion.objects.create(
                question_id=3,
                assignment=Assignment.objects.get(assignment_id=1),
            title="Hideauze",
            description="Where the Hideauze human?",
            true_choice="Yes, former humans",
            false_choice="No, aliens",
            answer=True,
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/assignment/1/question_true_false_modal',{
            'question_id':3,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'question_modal',response.content)

    def test_question_response_modal(self):
        ResponseQuestion.objects.create(
            question_id=4,
            assignment=Assignment.objects.get(assignment_id=1),
            title="Ice Age",
            description="Why did humanity migrate off-world?",
            answer="Because of solar hibernation causing Global Cooling on Earth.",
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/teacher/course/1/assignment/1/question_response_modal',{
            'question_id':4,
        },**kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'question_modal',response.content)

    def test_delete_question_with_incorrect_user(self):
        ResponseQuestion.objects.create(
            question_id=4,
            assignment=Assignment.objects.get(assignment_id=1),
            title="Ice Age",
            description="Why did humanity migrate off-world?",
            answer="Because of solar hibernation causing Global Cooling on Earth.",
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_trudy_client()
        response = client.post('/teacher/course/1/assignment/1/delete_question',{
            'question_id': 4,
            'question_type': settings.RESPONSE_QUESTION_TYPE,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['message'], 'unauthorized deletion')
        self.assertEqual(array['status'], 'failed')
