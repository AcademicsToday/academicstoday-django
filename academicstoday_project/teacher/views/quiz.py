from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import datetime
from registrar.models import Teacher
from registrar.models import Student
from registrar.models import Course
from registrar.models import Quiz
from registrar.models import TrueFalseQuestion
from teacher.forms import QuizForm
from teacher.forms import QuizQuestionTypeForm
from teacher.forms import TrueFalseQuestionForm


@login_required(login_url='/landpage')
def quizzes_page(request, course_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)

    return render(request, 'teacher/quiz/quiz_view.html',{
        'teacher' : teacher,
        'course' : course,
        'user' : request.user,
        'tab' : 'quizzes',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def quizzes_table(request, course_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)
    
    try:
        quizzes = Quiz.objects.filter(course=course).order_by('-quiz_num')
    except Quiz.DoesNotExist:
        quizzes = None
    return render(request, 'teacher/quiz/quiz_table.html',{
        'teacher' : teacher,
        'course' : course,
        'quizzes' : quizzes,
        'user' : request.user,
    })


@login_required(login_url='/landpage')
def quiz_modal(request, course_id):
    if request.method == u'POST':
        # Get the quiz_id of post and either create a brand new form
        # for the user, or load up existing one based on the database
        # data for the particular quiz.
        quiz_id = int(request.POST['quiz_id'])
        form = None
        if quiz_id > 0:
            quiz = Quiz.objects.get(quiz_id=quiz_id)
            form = QuizForm(instance=quiz)
        else:
            form = QuizForm()
        return render(request, 'teacher/quiz/quiz_modal.html',{
            'form' : form,
        })


@login_required(login_url='/landpage')
def save_quiz(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            course = Course.objects.get(id=course_id)
            quiz_id = int(request.POST['quiz_id'])
            form = None

            # If quiz already exists, then lets update only, else insert.
            if quiz_id > 0:
                quiz = Quiz.objects.get(quiz_id=quiz_id)
                form = QuizForm(instance=quiz, data=request.POST)
            else:
                form = QuizForm(request.POST, request.FILES)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.course = course
                instance.save()
                response_data = {'status' : 'success', 'message' : 'saved'}
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def delete_quiz(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deleting'}
    if request.is_ajax():
        if request.method == 'POST':
            quiz_id = int(request.POST['quiz_id'])
            try:
                Quiz.objects.get(quiz_id=quiz_id).delete()
                response_data = {'status' : 'success', 'message' : 'deleted'}
            except Quiz.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'record does not exist'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def quiz_page(request, course_id, quiz_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)
    quiz = Quiz.objects.get(quiz_id=quiz_id)

    # Load all true/false type questions for this quiz.
    try:
        tf_questions = TrueFalseQuestion.objects.filter(quiz=quiz).order_by('question_num')
    except TrueFalseQuestion.DoesNotExist:
        tf_questions = None

    return render(request, 'teacher/quiz/question_view.html',{
        'teacher' : teacher,
        'course' : course,
        'quiz' : quiz,
        'tf_questions' : tf_questions,
        'ESSAY_QUESTION_TYPE': settings.ESSAY_QUESTION_TYPE,
        'MULTIPLECHOICE_QUESTION_TYPE': settings.MULTIPLECHOICE_QUESTION_TYPE,
        'TRUEFALSE_QUESTION_TYPE': settings.TRUEFALSE_QUESTION_TYPE,
        'RESPONSE_QUESTION_TYPE': settings.RESPONSE_QUESTION_TYPE,
        'user' : request.user,
        'tab' : 'quiz',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


def questions_table(request, course_id, quiz_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)
    quiz = Quiz.objects.get(quiz_id=quiz_id)
    
    # Load all true/false type questions for this quiz.
    try:
        tf_questions = TrueFalseQuestion.objects.filter(quiz=quiz).order_by('question_num')
    except TrueFalseQuestion.DoesNotExist:
        tf_questions = None

    return render(request, 'teacher/quiz/question_table.html',{
        'teacher' : teacher,
        'course' : course,
        'quiz' : quiz,
        'tf_questions' : tf_questions,
        'ESSAY_QUESTION_TYPE': settings.ESSAY_QUESTION_TYPE,
        'MULTIPLECHOICE_QUESTION_TYPE': settings.MULTIPLECHOICE_QUESTION_TYPE,
        'TRUEFALSE_QUESTION_TYPE': settings.TRUEFALSE_QUESTION_TYPE,
        'RESPONSE_QUESTION_TYPE': settings.RESPONSE_QUESTION_TYPE,
        'user' : request.user,
    })


def question_type_modal(request, course_id, quiz_id):
    if request.is_ajax():
        if request.method == 'POST':
                quiz = Quiz.objects.get(quiz_id=quiz_id)
                form = QuizQuestionTypeForm()
                return render(request, 'teacher/quiz/question_modal.html',{
                    'quiz' : quiz,
                    'form' : form,
                    'ESSAY_QUESTION_TYPE': settings.ESSAY_QUESTION_TYPE,
                    'MULTIPLECHOICE_QUESTION_TYPE': settings.MULTIPLECHOICE_QUESTION_TYPE,
                    'TRUEFALSE_QUESTION_TYPE': settings.TRUEFALSE_QUESTION_TYPE,
                    'RESPONSE_QUESTION_TYPE': settings.RESPONSE_QUESTION_TYPE,
                    'user' : request.user,
                    'title' : 'New Question',
                    'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
                    'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
                })


def question_true_false_modal(request, course_id, quiz_id):
    if request.is_ajax():
        if request.method == 'POST':
                quiz = Quiz.objects.get(quiz_id=quiz_id)
                question_id = int(request.POST['question_id'])
                question = TrueFalseQuestion.objects.get(question_id=question_id)
                form = TrueFalseQuestionForm(instance=question)
                return render(request, 'teacher/quiz/question_modal.html',{
                    'quiz' : quiz,
                    'form' : form,
                    'ESSAY_QUESTION_TYPE': settings.ESSAY_QUESTION_TYPE,
                    'MULTIPLECHOICE_QUESTION_TYPE': settings.MULTIPLECHOICE_QUESTION_TYPE,
                    'TRUEFALSE_QUESTION_TYPE': settings.TRUEFALSE_QUESTION_TYPE,
                    'RESPONSE_QUESTION_TYPE': settings.RESPONSE_QUESTION_TYPE,
                    'user' : request.user,
                    'title' : 'True False Question',
                    'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
                    'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
                })


@login_required(login_url='/landpage')
def save_question(request, course_id, quiz_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            # Fetch objects
            course = Course.objects.get(id=course_id)
            teacher = Teacher.objects.get(user=request.user)
            quiz = Quiz.objects.get(quiz_id=quiz_id)

            # Fetch variables
            question_type = int(request.POST['question_type'])
            question_num = int(request.POST['question_num'])
            question_id = int(request.POST['question_id'])

            # DC: If question type is unsupported then error
            if question_type not in [settings.TRUEFALSE_QUESTION_TYPE]:
                response_data = {'status' : 'failed', 'message' : 'question type not supported'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")

            # If question_id equals zero then that means we need to create a new
            # entry, else we simply update the existing entry.
            if question_id == 0:
                # Create the question for the quiz depending on the
                # question type selected.
                if question_type == settings.TRUEFALSE_QUESTION_TYPE:
                    question = TrueFalseQuestion.objects.create(
                        quiz=quiz,
                        question_num=question_num
                    )
                    question.save()
                    response_data = {'status' : 'success', 'message' : 'question was saved'}
            else:
                # Update the question for the quiz depending on the
                # question type selected.
                question = None
                form = None
                if question_type == settings.TRUEFALSE_QUESTION_TYPE:
                    question = TrueFalseQuestion.objects.get(question_id=question_id)
                    form = TrueFalseQuestionForm(instance=question, data=request.POST)
                if form.is_valid():
                    form.save()
                    response_data = {'status' : 'success', 'message' : 'question was saved'}
                else:
                    response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def delete_question(request, course_id, quiz_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deleting'}
    if request.is_ajax():
        if request.method == 'POST':
            course = Course.objects.get(id=course_id)
            teacher = Teacher.objects.get(user=request.user)
            quiz = Quiz.objects.get(quiz_id=quiz_id)
            question_type = int(request.POST['question_type'])
            question_id = int(request.POST['question_id'])

            if course.teacher != teacher:
                response_data = {'status' : 'failed', 'message' : 'unauthorized deletion'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        
            # DC: If question type is unsupported then error
            if question_type not in [settings.TRUEFALSE_QUESTION_TYPE]:
                response_data = {'status' : 'failed', 'message' : 'question type not supported'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")

            # Delete our question.
            question = None
            if question_type == settings.TRUEFALSE_QUESTION_TYPE:
                question = TrueFalseQuestion.objects.get(question_id=question_id)
            question.delete()

            response_data = {'status' : 'success', 'message' : 'question was deleted'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
