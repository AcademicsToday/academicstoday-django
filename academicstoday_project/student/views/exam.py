from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

from registrar.models import Course
from registrar.models import MultipleChoiceQuestion
from registrar.models import MultipleChoiceSubmission
from registrar.models import Exam
from registrar.models import ExamSubmission
import json
import datetime

# Forms
from student.forms import EssaySubmissionForm
from student.forms import AssignmentSubmissionForm


# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#
# (2) JSON
# https://docs.djangoproject.com/en/1.7/topics/serialization/


@login_required(login_url='/landpage')
def exams_page(request, course_id):
    course = Course.objects.get(id=course_id)

    # Fetch all the assignments for this course.
    try:
        exams = Exam.objects.filter(course_id=course_id).order_by('order_num')
    except Exam.DoesNotExist:
        exams = None

    # Fetch all submitted assignments
    try:
        submitted_exams = ExamSubmission.objects.filter(course_id=course_id,
                                                        student_id=request.user.id)
    except ExamSubmission.DoesNotExist:
        submitted_exams = None

    # If the submissions & quizzes counts do not equal, then we have to
    # iterate through all the quizzes and create the missing 'submission'
    # entries for our system.
    if len(exams) != len(submitted_exams):
        for exam in exams:
            found_exam = False
            for submitted_exam in submitted_exams:
                if exam.id == submitted_exam.exam_id:
                    found_exam = True
            if not found_exam:
                submission = ExamSubmission.create(
                    student_id=request.user.id,
                    course_id=course_id,
                    exam_id=exam.id,
                    type=exam.type,
                    order_num=exam.order_num
                )
                submission.save()

    return render(request, 'course/exam/list.html',{
        'course' : course,
        'user' : request.user,
        'exams' : exams,
        'submitted_exams' : submitted_exams,
        'ESSAY_QUESTION_TYPE' : settings.ESSAY_QUESTION_TYPE,
        'MULTIPLECHOICE_QUESTION_TYPE' : settings.MULTIPLECHOICE_QUESTION_TYPE,
        'TRUEFALSE_QUESTION_TYPE' : settings.TRUEFALSE_QUESTION_TYPE,
        'RESPONSE_QUESTION_TYPE' : settings.RESPONSE_QUESTION_TYPE,
        'tab' : 'exams',
        'subtab' : '',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
    })


@login_required()
def exam_multiplechoice(request, course_id):
    if request.is_ajax():
        if request.method == 'POST':
            exam_id = int(request.POST['exam_id'])
            exam = Exam.objects.get(id=exam_id)
            try:
                questions = MultipleChoiceQuestion.objects.filter(
                    assignment_id=0,
                    exam_id=exam_id,
                    course_id=course_id,
                )
            except MultipleChoiceQuestion.DoesNotExist:
                questions = None

            return render(request, 'course/exam/mc_modal.html',{
                'exam' : exam,
                'questions' : questions,
            })


@login_required()
def submit_mc_exam_completion(request, course_id):
    # Update the 'submission_date' of our entry to indicate we
    # have finished the exam.
    submission = ExamSubmission.objects.get(
        exam_id=int(request.POST['exam_id']),
        student_id=int(request.POST['student_id']),
        course_id=int(request.POST['course_id']),
    )
    submission.submission_date = datetime.datetime.utcnow()
    submission.save()

    response_data = {'status' : 'success', 'message' : ''}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def submit_mc_exam_answer(request, course_id):
    if request.is_ajax():
        if request.method == 'POST':
            exam_id = int(request.POST['exam_id'])
            student_id = int(request.POST['student_id'])
            course_id = int(request.POST['course_id'])
            question_num = int(request.POST['num'])
            key = request.POST['key']
            value = request.POST['value']
            # Fetch question and error if not found.
            try:
                question = MultipleChoiceQuestion.objects.get(
                    assignment_id=0,
                    course_id=course_id,
                    question_num=question_num,
                    exam_id=exam_id,
                )
            except MultipleChoiceQuestion.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'cannot find question'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")

            # Fetch submission and create new submission if not found.
            try:
                submission = MultipleChoiceSubmission.objects.get(
                    student_id=student_id,
                    assignment_id=0,
                    course_id=course_id,
                    question_num=question_num,
                    exam_id=exam_id,
                )
            except MultipleChoiceSubmission.DoesNotExist:
                submission = MultipleChoiceSubmission.create(
                    student_id=student_id,
                    assignment_id=0,
                    course_id=course_id,
                    question_num=question_num,
                    exam_id=exam_id,
                )
                submission.save()

            # Convert JSON string into Python array
            answers = json.loads(submission.json_answers)

            # Append or remove the answers json entry from the submission object.
            found_value = answers.get(key, None)
            if found_value == value:
                answers.pop(key, None)
            else:
                answers[key] = value

            # Convert back into JSON string and save
            submission.json_answers = json.dumps(answers)
            submission.save()

            response_data = {'status' : 'success', 'message' : ''}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

    response_data = {'status' : 'failed', 'message' : 'error submitting'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def exam_delete(request, course_id):
    if request.is_ajax():
        if request.method == 'POST':
            student_id = int(request.POST['student_id'])
            exam_id = int(request.POST['exam_id'])
            exam_type = int(request.POST['exam_type'])

            # Update the 'submission_date' of our entry to indicate we
            # have finished the exam.
            submission = ExamSubmission.objects.get(
                exam_id=int(request.POST['exam_id']),
                student_id=int(request.POST['student_id']),
                course_id=int(request.POST['course_id'])
            )
            submission.submission_date = None
            submission.save()

            if exam_type == settings.MULTIPLECHOICE_QUESTION_TYPE:
                try:
                    MultipleChoiceSubmission.objects.filter(
                        assignment_id=0,
                        exam_id=exam_id,
                        student_id=student_id,
                        course_id=course_id,
                    ).delete()
                    response_data = {'status' : 'success', 'message' : 'assignment was deleted'}
                except MultipleChoiceSubmission.DoesNotExist:
                    response_data = {'status' : 'failed', 'message' : 'assignment not found'}
            else:
                response_data = {'status' : 'success', 'message' : ''}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    response_data = {'status' : 'failed', 'message' : 'unknown error with deletion'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
