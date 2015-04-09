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
from registrar.models import Assignment
from registrar.models import AssignmentSubmission
from registrar.models import Quiz
from registrar.models import QuizSubmission
from registrar.models import Exam
from registrar.models import ExamSubmission
from registrar.models import EssayQuestion
from registrar.models import EssaySubmission
from registrar.models import MultipleChoiceQuestion
from registrar.models import MultipleChoiceSubmission
from registrar.models import ResponseQuestion
from registrar.models import ResponseSubmission
from registrar.models import TrueFalseQuestion
from registrar.models import TrueFalseSubmission
from registrar.models import PeerReview
from student.views import assignment
from student.views import quiz
from student.views import exam
from student.views import credit


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class CreditTestCase(TestCase):
    def tearDown(self):
        courses = Course.objects.all()
        for course in courses:
            course.delete()
        User.objects.get(email=TEST_USER_EMAIL).delete()
    
    def setUp(self):
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
        course = Course.objects.create(
            id=1,
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
            teacher=teacher,
        )

        # Create our assignment(s)
        assignment = Assignment.objects.create(
            assignment_id=1,
            assignment_num=1,
            title="Hideauze",
            description="Anime related assignment.",
            worth=25,
            course=course,
        )

        # Create questions
        EssayQuestion.objects.create(
            question_id=1,
            assignment=assignment,
            title="Evolvers",
            description="Write an essay about the Evolvers.",
        )
        MultipleChoiceQuestion.objects.create(
            question_id=2,
            assignment=assignment,
            title="Hideauze",
            description="Who where the Hideauze?",
            a="Former Humans",
            a_is_correct=True,
            b="Aliens",
            b_is_correct=False,
            c="Magical or Supernatural Creatures",
            c_is_correct=False,
            d="Dark Elves",
            d_is_correct=False,
            e="Heavenly Creatures",
            e_is_correct=False,
        )
        TrueFalseQuestion.objects.create(
            question_id=3,
            assignment=assignment,
            title="Hideauze",
            description="Where the Hideauze human?",
            true_choice="Yes, former humans",
            false_choice="No, aliens",
            answer=True,
        )
        ResponseQuestion.objects.create(
            question_id=4,
            assignment=assignment,
            title="Hideauze",
            description="Why did humanity migrate off-world?",
            answer="Because of solar hibernation causing Global Cooling on Earth.",
        )

        # Create our quiz
        Quiz.objects.create(
            quiz_id=1,
            quiz_num=1,
            title="Hideauze",
            description="Anime related assignment.",
            worth=25,
            course=course,
        )
        quiz = Quiz.objects.get(quiz_id=1)
        TrueFalseQuestion.objects.create(
            question_id=5,
            quiz=quiz,
            title="Hideauze",
            description="Where the Hideauze human?",
            true_choice="Yes, former humans",
            false_choice="No, aliens",
            answer=True,
        )
            
        # Create our Exam
        Exam.objects.create(
            exam_id=1,
            exam_num=1,
            title="Hideauze",
            description="Anime related assignment.",
            worth=50,
            course=course,
            is_final=True,
        )
        exam = Exam.objects.get(exam_id=1)
        MultipleChoiceQuestion.objects.create(
            question_id=6,
            exam=exam,
            title="Hideauze",
            description="Who where the Hideauze?",
            a="Former Humans",
            a_is_correct=True,
            b="Aliens",
            b_is_correct=False,
            c="Magical or Supernatural Creatures",
            c_is_correct=False,
            d="Orcs",
            d_is_correct=False,
            e="Heavenly Creatures",
            e_is_correct=False,
        )

    def get_logged_in_client(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        return client

    def test_url_resolves_to_credit_page_view(self):
        found = resolve('/course/1/credit')
        self.assertEqual(found.func, credit.credit_page)

    def test_credit_page_with_no_submissions(self):
        client = self.get_logged_in_client()
        response = client.post('/course/1/credit')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'ajax_submit_credit_application();',response.content)

    def test_url_resolves_to_submit_json(self):
        found = resolve('/course/1/submit_credit_application')
        self.assertEqual(found.func, credit.submit_credit_application)

    def test_submit_credit_application_on_no_failing_criteria(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        response = client.post('/course/1/submit_credit_application',{
            'assignment_id': 1,
        }, **kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['status'], 'failure')
        self.assertEqual(array['message'], 'you need to pass with at minimum 50%')

    def test_submit_credit_application_on_passing_criteria_without_peer_reviews(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        
        # Setup Failing
        # Assignment
        file_path = settings.MEDIA_ROOT + '/sample.pdf'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            client.post('/course/1/assignment/1/submit_e_assignment_answer',{
                'question_id': 1,
                'file': fp
            }, **kwargs)
        client.post('/course/1/assignment/1/submit_mc_assignment_answer',{
            'question_id': 2,
            'answer': 'A',
        }, **kwargs)
        client.post('/course/1/assignment/1/submit_tf_assignment_answer',{
            'question_id': 3,
            'answer': 'true',
        }, **kwargs)
        client.post('/course/1/assignment/1/submit_r_assignment_answer',{
            'question_id': 4,
            'answer': 'Because of Global Cooling caused by abnormal solar hibernation.',
        }, **kwargs)
        client.post('/course/1/assignment/1/submit_assignment',{}, **kwargs)

        # Quiz
        client.post('/course/1/quiz/1/submit_tf_quiz_answer',{
            'question_id': 5,
            'answer': 'true',
        }, **kwargs)
        client.post('/course/1/quiz/1/submit_quiz',{}, **kwargs)

        # Exam
        response = client.post('/course/1/exam/1/submit_mc_exam_answer',{
            'question_id': 6,
            'answer': 'A',
        }, **kwargs)
        client.post('/course/1/exam/1/submit_exam',{}, **kwargs)

        # Test
        response = client.post('/course/1/submit_credit_application',{
            'assignment_id': 1,
        }, **kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'credit granted')

        # Cleanup
        try:
            EssaySubmission.objects.get(submission_id=1).delete()
        except EssaySubmission.DoesNotExist:
            pass
        try:
            EssaySubmission.objects.get(submission_id=2).delete()
        except EssaySubmission.DoesNotExist:
            pass

    def test_submit_credit_application_on_passing_criteria_with_peer_reviews(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = self.get_logged_in_client()
        
        # Setup Failing
        # Assignment
        file_path = settings.MEDIA_ROOT + '/sample.pdf'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            client.post('/course/1/assignment/1/submit_e_assignment_answer',{
                'question_id': 1,
                'file': fp
            }, **kwargs)
        client.post('/course/1/assignment/1/submit_mc_assignment_answer',{
            'question_id': 2,
            'answer': 'A',
        }, **kwargs)
        client.post('/course/1/assignment/1/submit_tf_assignment_answer',{
            'question_id': 3,
            'answer': 'true',
        }, **kwargs)
        client.post('/course/1/assignment/1/submit_r_assignment_answer',{
            'question_id': 4,
            'answer': 'Because of Global Cooling caused by abnormal solar hibernation.',
        }, **kwargs)
        client.post('/course/1/assignment/1/submit_assignment',{}, **kwargs)
                        
        # Quiz
        client.post('/course/1/quiz/1/submit_tf_quiz_answer',{
            'question_id': 5,
            'answer': 'true',
        }, **kwargs)
        client.post('/course/1/quiz/1/submit_quiz',{}, **kwargs)
                                
        # Exam
        response = client.post('/course/1/exam/1/submit_mc_exam_answer',{
            'question_id': 6,
            'answer': 'A',
        }, **kwargs)
        client.post('/course/1/exam/1/submit_exam',{}, **kwargs)
        
        # Peer Reviews
        client.post('/course/1/peer_review/1/save_peer_review',{
            'question_id': 1,
            'question_type': settings.ESSAY_QUESTION_TYPE,
            'submission_id': 1,
            'marks': 5,
        },**kwargs)
        client.post('/course/1/peer_review/1/save_peer_review',{
            'question_id': 4,
            'question_type': settings.RESPONSE_QUESTION_TYPE,
            'submission_id': 1,
            'marks': 5,
        },**kwargs)
        
        # Test
        response = client.post('/course/1/submit_credit_application',{
            'assignment_id': 1,
        }, **kwargs)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'credit granted')
                                                                
        # Cleanup
        try:
            EssaySubmission.objects.get(submission_id=1).delete()
        except EssaySubmission.DoesNotExist:
            pass
        try:
            EssaySubmission.objects.get(submission_id=2).delete()
        except EssaySubmission.DoesNotExist:
            pass