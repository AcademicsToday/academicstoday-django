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
from registrar.models import Exam
from registrar.models import EssayQuestion
from registrar.models import MultipleChoiceQuestion
from registrar.models import TrueFalseQuestion
from registrar.models import ResponseQuestion
from teacher.forms import ExamForm
from teacher.forms import ExamQuestionTypeForm
from teacher.forms import MultipleChoiceQuestionForm


@login_required(login_url='/landpage')
def exams_page(request, course_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)

    try:
        exams = Exam.objects.filter(course=course).order_by('-exam_num')
    except Exam.DoesNotExist:
        exams = None
    return render(request, 'teacher/exam/exam_view.html',{
        'teacher' : teacher,
        'course' : course,
        'exams' : exams,
        'user' : request.user,
        'tab' : 'exams',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })

@login_required(login_url='/landpage')
def exams_table(request, course_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)
    
    try:
        exams = Exam.objects.filter(course=course).order_by('-exam_num')
    except Exam.DoesNotExist:
        exams = None
    return render(request, 'teacher/exam/exam_table.html',{
        'teacher' : teacher,
        'course' : course,
        'exams' : exams,
        'user' : request.user,
    })


@login_required(login_url='/landpage')
def exam_modal(request, course_id):
    if request.method == u'POST':
        # Get the exam_id of post and either create a brand new form
        # for the user, or load up existing one based on the database
        # data for the particular exam.
        exam_id = int(request.POST['exam_id'])
        form = None
        if exam_id > 0:
            exam = Exam.objects.get(exam_id=exam_id)
            form = ExamForm(instance=exam)
        else:
            form = ExamForm()
        return render(request, 'teacher/exam/exam_modal.html',{
            'form' : form,
        })


@login_required(login_url='/landpage')
def save_exam(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            course = Course.objects.get(id=course_id)
            exam_id = int(request.POST['exam_id'])
            form = None

            # If exam already exists, then lets update only, else insert.
            if exam_id > 0:
                exam = Exam.objects.get(exam_id=exam_id)
                form = ExamForm(instance=exam, data=request.POST)
            else:
                form = ExamForm(request.POST, request.FILES)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.course = course
                instance.save()
                response_data = {'status' : 'success', 'message' : 'saved'}
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def delete_exam(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deleting'}
    if request.is_ajax():
        if request.method == 'POST':
            exam_id = int(request.POST['exam_id'])
            teacher = Teacher.objects.get(user=request.user)
            try:
                exam = Exam.objects.get(exam_id=exam_id)
                if exam.course.teacher == teacher:
                    exam.delete()
                    response_data = {'status' : 'success', 'message' : 'deleted'}
                else:
                     response_data = {'status' : 'failed', 'message' : 'unauthorized deletion'}
            except Exam.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'record does not exist'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def exam_page(request, course_id, exam_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)
    exam = Exam.objects.get(exam_id=exam_id)

    # Load all multiple-choice type questions for this exam.
    try:
        mc_questions = MultipleChoiceQuestion.objects.filter(exam=exam).order_by('question_num')
    except MultipleChoiceQuestion.DoesNotExist:
        mc_questions = None

    return render(request, 'teacher/exam/question_view.html',{
        'teacher' : teacher,
        'course' : course,
        'exam' : exam,
        'mc_questions' : mc_questions,
        'ESSAY_QUESTION_TYPE': settings.ESSAY_QUESTION_TYPE,
        'MULTIPLECHOICE_QUESTION_TYPE': settings.MULTIPLECHOICE_QUESTION_TYPE,
        'TRUEFALSE_QUESTION_TYPE': settings.TRUEFALSE_QUESTION_TYPE,
        'RESPONSE_QUESTION_TYPE': settings.RESPONSE_QUESTION_TYPE,
        'user' : request.user,
        'tab' : 'exam',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


def questions_table(request, course_id, exam_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)
    exam = Exam.objects.get(exam_id=exam_id)
    
    # Load all multiple-choice type questions for this exam.
    try:
        mc_questions = MultipleChoiceQuestion.objects.filter(exam=exam).order_by('question_num')
    except MultipleChoiceQuestion.DoesNotExist:
        mc_questions = None

    return render(request, 'teacher/exam/question_table.html',{
        'teacher' : teacher,
        'course' : course,
        'exam' : exam,
        'mc_questions' : mc_questions,
        'ESSAY_QUESTION_TYPE': settings.ESSAY_QUESTION_TYPE,
        'MULTIPLECHOICE_QUESTION_TYPE': settings.MULTIPLECHOICE_QUESTION_TYPE,
        'TRUEFALSE_QUESTION_TYPE': settings.TRUEFALSE_QUESTION_TYPE,
        'RESPONSE_QUESTION_TYPE': settings.RESPONSE_QUESTION_TYPE,
        'user' : request.user,
    })


def question_type_modal(request, course_id, exam_id):
    if request.is_ajax():
        if request.method == 'POST':
                exam = Exam.objects.get(exam_id=exam_id)
                form = ExamQuestionTypeForm()
                return render(request, 'teacher/exam/question_modal.html',{
                    'exam' : exam,
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


def question_multiple_choice_modal(request, course_id, exam_id):
    if request.is_ajax():
        if request.method == 'POST':
                exam = Exam.objects.get(exam_id=exam_id)
                question_id = int(request.POST['question_id'])
                question = MultipleChoiceQuestion.objects.get(question_id=question_id)
                form = MultipleChoiceQuestionForm(instance=question)
                return render(request, 'teacher/exam/question_modal.html',{
                    'exam' : exam,
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


@login_required(login_url='/landpage')
def save_question(request, course_id, exam_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            # Fetch objects
            course = Course.objects.get(id=course_id)
            teacher = Teacher.objects.get(user=request.user)
            exam = Exam.objects.get(exam_id=exam_id)

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
                # Create the question for the exam depending on the
                # question type selected.
                if question_type == settings.MULTIPLECHOICE_QUESTION_TYPE:
                    question = MultipleChoiceQuestion.objects.create(
                        exam=exam,
                        question_num=question_num
                    )
                    question.save()
                    response_data = {'status' : 'success', 'message' : 'question was saved'}
            else:
                # Update the question for the exam depending on the
                # question type selected.
                question = None
                form = None
                if question_type == settings.MULTIPLECHOICE_QUESTION_TYPE:
                    question = MultipleChoiceQuestion.objects.get(question_id=question_id)
                    form = MultipleChoiceQuestionForm(instance=question, data=request.POST)
                if form.is_valid():
                    form.save()
                    response_data = {'status' : 'success', 'message' : 'question was saved'}
                else:
                    response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def delete_question(request, course_id, exam_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deleting'}
    if request.is_ajax():
        if request.method == 'POST':
            course = Course.objects.get(id=course_id)
            teacher = Teacher.objects.get(user=request.user)
            exam = Exam.objects.get(exam_id=exam_id)
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
            if question_type == settings.MULTIPLECHOICE_QUESTION_TYPE:
                question = MultipleChoiceQuestion.objects.get(question_id=question_id)
            question.delete()

            response_data = {'status' : 'success', 'message' : 'question was deleted'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
