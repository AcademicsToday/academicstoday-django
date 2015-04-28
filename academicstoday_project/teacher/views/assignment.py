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
from teacher.forms import AssignmentQuestionTypeForm
from teacher.forms import EssayQuestionForm
from teacher.forms import MultipleChoiceQuestionForm
from teacher.forms import TrueFalseQuestionForm
from teacher.forms import ResponseQuestionForm


@login_required(login_url='/landpage')
def assignments_page(request, course_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)

    try:
        assignments = Assignment.objects.filter(course=course).order_by('-assignment_num')
    except Assignment.DoesNotExist:
        assignments = None
    return render(request, 'teacher/assignment/assignment_view.html',{
        'teacher' : teacher,
        'course' : course,
        'assignments' : assignments,
        'user' : request.user,
        'tab' : 'assignments',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def assignments_table(request, course_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)
    
    try:
        assignments = Assignment.objects.filter(course=course).order_by('-assignment_num')
    except Assignment.DoesNotExist:
        assignments = None
    return render(request, 'teacher/assignment/assignment_table.html',{
        'teacher' : teacher,
        'course' : course,
        'assignments' : assignments,
        'user' : request.user,
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
            teacher = Teacher.objects.get(user=request.user)
            try:
                assignment = Assignment.objects.get(assignment_id=assignment_id)
                if assignment.course.teacher == teacher:
                    assignment.delete()
                    response_data = {'status' : 'success', 'message' : 'assignment was deleted'}
                else:
                    response_data = {'status' : 'failed', 'message' : 'unauthorized deletion'}
            except Assignment.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'record not found'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def assignment_page(request, course_id, assignment_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)
    assignment = Assignment.objects.get(assignment_id=assignment_id)

    return render(request, 'teacher/assignment/question_view.html',{
        'teacher' : teacher,
        'course' : course,
        'assignment' : assignment,
        'ESSAY_QUESTION_TYPE': settings.ESSAY_QUESTION_TYPE,
        'MULTIPLECHOICE_QUESTION_TYPE': settings.MULTIPLECHOICE_QUESTION_TYPE,
        'TRUEFALSE_QUESTION_TYPE': settings.TRUEFALSE_QUESTION_TYPE,
        'RESPONSE_QUESTION_TYPE': settings.RESPONSE_QUESTION_TYPE,
        'user' : request.user,
        'tab' : 'assignment',
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })

def questions_table(request, course_id, assignment_id):
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
    
    # Load all true/false type questions for this assignment.
    try:
        tf_questions = TrueFalseQuestion.objects.filter(assignment=assignment).order_by('question_num')
    except TrueFalseQuestion.DoesNotExist:
        tf_questions = None
    
    # Load all response type questions for this assignment.
    try:
        r_questions = ResponseQuestion.objects.filter(assignment=assignment).order_by('question_num')
    except ResponseQuestion.DoesNotExist:
        r_questions = None
    
    return render(request, 'teacher/assignment/question_table.html',{
        'teacher' : teacher,
        'course' : course,
        'assignment' : assignment,
        'essay_questions' : essay_questions,
        'mc_questions' : mc_questions,
        'tf_questions' : tf_questions,
        'r_questions' : r_questions,
        'ESSAY_QUESTION_TYPE': settings.ESSAY_QUESTION_TYPE,
        'MULTIPLECHOICE_QUESTION_TYPE': settings.MULTIPLECHOICE_QUESTION_TYPE,
        'TRUEFALSE_QUESTION_TYPE': settings.TRUEFALSE_QUESTION_TYPE,
        'RESPONSE_QUESTION_TYPE': settings.RESPONSE_QUESTION_TYPE,
        'user' : request.user,
        'tab' : 'assignment',
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


def question_type_modal(request, course_id, assignment_id):
    if request.is_ajax():
        if request.method == 'POST':
                assignment = Assignment.objects.get(assignment_id=assignment_id)
                form = AssignmentQuestionTypeForm()
                return render(request, 'teacher/assignment/question_modal.html',{
                    'assignment' : assignment,
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
                    'ESSAY_QUESTION_TYPE': settings.ESSAY_QUESTION_TYPE,
                    'MULTIPLECHOICE_QUESTION_TYPE': settings.MULTIPLECHOICE_QUESTION_TYPE,
                    'TRUEFALSE_QUESTION_TYPE': settings.TRUEFALSE_QUESTION_TYPE,
                    'RESPONSE_QUESTION_TYPE': settings.RESPONSE_QUESTION_TYPE,
                    'user' : request.user,
                    'title' : 'Essay Question',
                    'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
                    'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
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
                    'ESSAY_QUESTION_TYPE': settings.ESSAY_QUESTION_TYPE,
                    'MULTIPLECHOICE_QUESTION_TYPE': settings.MULTIPLECHOICE_QUESTION_TYPE,
                    'TRUEFALSE_QUESTION_TYPE': settings.TRUEFALSE_QUESTION_TYPE,
                    'RESPONSE_QUESTION_TYPE': settings.RESPONSE_QUESTION_TYPE,
                    'user' : request.user,
                    'title' : 'Multiple Choice Question',
                    'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
                    'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
                })


def question_true_false_modal(request, course_id, assignment_id):
    if request.is_ajax():
        if request.method == 'POST':
                assignment = Assignment.objects.get(assignment_id=assignment_id)
                question_id = int(request.POST['question_id'])
                question = TrueFalseQuestion.objects.get(question_id=question_id)
                form = TrueFalseQuestionForm(instance=question)
                return render(request, 'teacher/assignment/question_modal.html',{
                    'assignment' : assignment,
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


def question_response_modal(request, course_id, assignment_id):
    if request.is_ajax():
        if request.method == 'POST':
                assignment = Assignment.objects.get(assignment_id=assignment_id)
                question_id = int(request.POST['question_id'])
                question = ResponseQuestion.objects.get(question_id=question_id)
                form = ResponseQuestionForm(instance=question)
                return render(request, 'teacher/assignment/question_modal.html',{
                    'assignment' : assignment,
                    'form' : form,
                    'ESSAY_QUESTION_TYPE': settings.ESSAY_QUESTION_TYPE,
                    'MULTIPLECHOICE_QUESTION_TYPE': settings.MULTIPLECHOICE_QUESTION_TYPE,
                    'TRUEFALSE_QUESTION_TYPE': settings.TRUEFALSE_QUESTION_TYPE,
                    'RESPONSE_QUESTION_TYPE': settings.RESPONSE_QUESTION_TYPE,
                    'user' : request.user,
                    'title' : 'Response Question',
                    'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
                    'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
                })


@login_required(login_url='/landpage')
def save_question(request, course_id, assignment_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            # Fetch objects
            course = Course.objects.get(id=course_id)
            teacher = Teacher.objects.get(user=request.user)
            assignment = Assignment.objects.get(assignment_id=assignment_id)

            # Fetch variables
            question_type = int(request.POST['question_type'])
            question_num = int(request.POST['question_num'])
            question_id = int(request.POST['question_id'])

            # DC: If question type is unsupported then error
            if question_type not in settings.QUESTION_TYPES:
                response_data = {'status' : 'failed', 'message' : 'question type not supported'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")

            # If question_id equals zero then that means we need to create a new
            # entry, else we simply update the existing entry.
            if question_id == 0:
                # Create the question for the assignment depending on the
                # question type selected.
                if question_type == settings.ESSAY_QUESTION_TYPE:
                    question = EssayQuestion.objects.create(
                        assignment=assignment,
                        question_num=question_num
                    )
                    question.save()
                elif question_type == settings.MULTIPLECHOICE_QUESTION_TYPE:
                    question = MultipleChoiceQuestion.objects.create(
                        assignment=assignment,
                        question_num=question_num
                    )
                    question.save()
                elif question_type == settings.TRUEFALSE_QUESTION_TYPE:
                    question = TrueFalseQuestion.objects.create(
                        assignment=assignment,
                        question_num=question_num
                    )
                    question.save()
                elif question_type == settings.RESPONSE_QUESTION_TYPE:
                    question = ResponseQuestion.objects.create(
                        assignment=assignment,
                        question_num=question_num
                    )
                    question.save()
                # Return positive response.
                response_data = {'status' : 'success', 'message' : 'question was saved'}
            else:
                # Update the question for the assignment depending on the
                # question type selected.
                question = None
                form = None
                if question_type == settings.ESSAY_QUESTION_TYPE:
                    question = EssayQuestion.objects.get(question_id=question_id)
                    form = EssayQuestionForm(instance=question, data=request.POST)
                elif question_type == settings.MULTIPLECHOICE_QUESTION_TYPE:
                    question = MultipleChoiceQuestion.objects.get(question_id=question_id)
                    form = MultipleChoiceQuestionForm(instance=question, data=request.POST)
                elif question_type == settings.TRUEFALSE_QUESTION_TYPE:
                    question = TrueFalseQuestion.objects.get(question_id=question_id)
                    form = TrueFalseQuestionForm(instance=question, data=request.POST)
                elif question_type == settings.RESPONSE_QUESTION_TYPE:
                    question = ResponseQuestion.objects.get(question_id=question_id)
                    form = ResponseQuestionForm(instance=question, data=request.POST)
                if form.is_valid():
                    form.save()
                    response_data = {'status' : 'success', 'message' : 'question was saved'}
                else:
                    response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
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

            if course.teacher != teacher:
                response_data = {'status' : 'failed', 'message' : 'unauthorized deletion'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")

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

            response_data = {'status' : 'success', 'message' : 'question was deleted'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
