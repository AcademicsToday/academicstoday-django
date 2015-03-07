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
from registrar.models import Assignment
from registrar.models import EssayQuestion
from registrar.models import MultipleChoiceQuestion
from registrar.models import TrueFalseQuestion
from registrar.models import ResponseQuestion
from teacher.forms import AssignmentForm
from teacher.forms import QuestionTypeForm
from teacher.forms import EssayQuestionForm
from teacher.forms import MultipleChoiceQuestionForm

# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#

@login_required(login_url='/landpage')
def assignments_page(request, course_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)

    try:
        assignments = Assignment.objects.filter(course=course).order_by('-assignment_num')
    except Assignment.DoesNotExist:
        assignments = None
    return render(request, 'teacher/assignment/assignment_list.html',{
        'teacher' : teacher,
        'course' : course,
        'assignments' : assignments,
        'user' : request.user,
        'tab' : 'assignments',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
    })

@login_required(login_url='/landpage')
def assignment_modal(request, course_id):
    if request.method == u'POST':
        # Get the assignment_id of post and either create a brand new form
        # for the user, or load up existing one based on the database
        # data for the particular assignment.
        assignment_id = int(request.POST['assignment_id'])
        form = None
        if assignment_id > 0:
            assignment = Assignment.objects.get(assignment_id=assignment_id)
            form = AssignmentForm(instance=assignment)
        else:
            form = AssignmentForm()
        return render(request, 'teacher/assignment/assignment_modal.html',{
            'form' : form,
        })


@login_required(login_url='/landpage')
def save_assignment(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            course = Course.objects.get(id=course_id)
            assignment_id = int(request.POST['assignment_id'])
            form = None

            # If assignment already exists, then lets update only, else insert.
            if assignment_id > 0:
                assignment = Assignment.objects.get(assignment_id=assignment_id)
                form = AssignmentForm(instance=assignment, data=request.POST)
            else:
                form = AssignmentForm(request.POST, request.FILES)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.course = course
                instance.save()
                response_data = {'status' : 'success', 'message' : 'saved'}
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def delete_assignment(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deleting'}
    if request.is_ajax():
        if request.method == 'POST':
            assignment_id = int(request.POST['assignment_id'])
            assignment = Assignment.objects.get(assignment_id=assignment_id)
            assignment.delete()
            response_data = {'status' : 'success', 'message' : 'deleted'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def assignment_page(request, course_id, assignment_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)
    assignment = Assignment.objects.get(assignment_id=assignment_id)

    # Load all essay type questions for this assignment.
    try:
        essay_questions = EssayQuestion.objects.filter(assignment=assignment).order_by('question_num')
    except EssayQuestion.DoesNotExist:
        essay_questions = None

    # Load all multiple-choice type questions for this assignment.
    try:
        mc_questions = MultipleChoiceQuestion.objects.filter(assignment=assignment).order_by('question_num')
    except MultipleChoiceQuestion.DoesNotExist:
        mc_questions = None

    return render(request, 'teacher/assignment/question_list.html',{
        'teacher' : teacher,
        'course' : course,
        'assignment' : assignment,
        'essay_questions' : essay_questions,
        'mc_questions' : mc_questions,
        'ESSAY_QUESTION_TYPE': settings.ESSAY_QUESTION_TYPE,
        'MULTIPLECHOICE_QUESTION_TYPE': settings.MULTIPLECHOICE_QUESTION_TYPE,
        'user' : request.user,
        'tab' : 'assignments',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
    })

def question_type_modal(request, course_id, assignment_id):
    if request.is_ajax():
        if request.method == 'POST':
                assignment = Assignment.objects.get(assignment_id=assignment_id)
                form = QuestionTypeForm()
                return render(request, 'teacher/assignment/question_modal.html',{
                    'assignment' : assignment,
                    'form' : form,
                    'user' : request.user,
                    'title' : 'New Question',
                    'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
                    'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
                })


def question_essay_modal(request, course_id, assignment_id):
    if request.is_ajax():
        if request.method == 'POST':
                assignment = Assignment.objects.get(assignment_id=assignment_id)
                question_id = int(request.POST['question_id'])
                question = EssayQuestion.objects.get(question_id=question_id)
                form = EssayQuestionForm(instance=question)
                return render(request, 'teacher/assignment/question_modal.html',{
                    'assignment' : assignment,
                    'form' : form,
                    'user' : request.user,
                    'title' : 'Essay Question',
                    'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
                    'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
                })


def question_multiple_choice_modal(request, course_id, assignment_id):
    if request.is_ajax():
        if request.method == 'POST':
                assignment = Assignment.objects.get(assignment_id=assignment_id)
                question_id = int(request.POST['question_id'])
                question = MultipleChoiceQuestion.objects.get(question_id=question_id)
                form = MultipleChoiceQuestionForm(instance=question)
                return render(request, 'teacher/assignment/question_modal.html',{
                    'assignment' : assignment,
                    'form' : form,
                    'user' : request.user,
                    'title' : 'Multiple Choice Question',
                    'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
                    'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
                })


@login_required(login_url='/landpage')
def insert_question(request, course_id, assignment_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            course = Course.objects.get(id=course_id)
            teacher = Teacher.objects.get(user=request.user)
            assignment = Assignment.objects.get(assignment_id=assignment_id)
            question_type = int(request.POST['type'])
            question_num = int(request.POST['num'])

            # DC: If question type is unsupported then error
            if question_type not in settings.QUESTION_TYPES:
                response_data = {'status' : 'failed', 'message' : 'question type not supported'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")

            # Create the question for the assignment depending on the question
            # type selected.
            if question_type == settings.ESSAY_QUESTION_TYPE:
                question = EssayQuestion.objects.create(
                    course=course,
                    assignment=assignment,
                    question_num=question_num
                )
                question.save()
            elif question_type == settings.MULTIPLECHOICE_QUESTION_TYPE:
                question = MultipleChoiceQuestion.objects.create(
                    course=course,
                    assignment=assignment,
                    question_num=question_num
                )
                question.save()
            elif question_type == settings.TRUEFALSE_QUESTION_TYPE:
                question = TrueFalseQuestion.objects.create(
                    course=course,
                    assignment=assignment,
                    question_num=question_num
                )
                question.save()
            elif question_type == settings.RESPONSE_QUESTION_TYPE:
                question = ResponseQuestion.objects.create(
                    course=course,
                    assignment=assignment,
                    question_num=question_num
                )
                question.save()

            response_data = {'status' : 'success', 'message' : 'question was inserted'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def delete_question(request, course_id, assignment_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deleting'}
    if request.is_ajax():
        if request.method == 'POST':
            course = Course.objects.get(id=course_id)
            teacher = Teacher.objects.get(user=request.user)
            assignment = Assignment.objects.get(assignment_id=assignment_id)
            question_type = int(request.POST['question_type'])
            question_id = int(request.POST['question_id'])

            # DC: If question type is unsupported then error
            if question_type not in settings.QUESTION_TYPES:
                response_data = {'status' : 'failed', 'message' : 'question type not supported'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")

            # Delete our question.
            question = None
            if question_type == settings.ESSAY_QUESTION_TYPE:
                question = EssayQuestion.objects.get(question_id=question_id)
            elif question_type == settings.MULTIPLECHOICE_QUESTION_TYPE:
                question = MultipleChoiceQuestion.objects.get(question_id=question_id)
            elif question_type == settings.TRUEFALSE_QUESTION_TYPE:
                question = TrueFalseQuestion.objects.get(question_id=question_id)
            elif question_type == settings.RESPONSE_QUESTION_TYPE:
                question = ResponseQuestion.objects.get(question_id=question_id)
            question.delete()

            response_data = {'status' : 'success', 'message' : 'question was inserted'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
