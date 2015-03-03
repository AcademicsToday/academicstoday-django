from django.shortcuts import render
from django.core import serializers
from registrar.models import Course
from registrar.models import CourseEnrollment
from course.models import Announcement
from course.models import Syllabus
from course.models import Policy
from course.models import Week
from course.models import Lecture
from course.models import Assignment
from course.models import AssignmentSubmission
from course.models import EssayQuestion
from course.models import EssaySubmission
from course.models import MultipleChoiceQuestion
from course.models import MultipleChoiceSubmission
from course.models import ResponseQuestion
from course.models import ResponseSubmission
from course.models import TrueFalseQuestion
from course.models import TrueFalseSubmission
from course.models import Quiz
from course.models import QuizSubmission
from course.models import Exam
from course.models import ExamSubmission
import json
import datetime
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings


# Forms
from course.forms import EssaySubmissionForm
from course.forms import AssignmentSubmissionForm


# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#
# (2) JSON
# https://docs.djangoproject.com/en/1.7/topics/serialization/



css_library_urls = ["js/jquery/1.11.1/jquery-ui.css",
                    "js/bootstrap/3.3.2/css/bootstrap.min.css",
                    "js/font-awesome/4.2.0/css/font-awesome.css",
                    "js/font-awesome/4.2.0/css/font-awesome.min.css",
                    "css/sb-admin.css"]

js_library_urls = ["js/jquery/1.11.1/jquery.min.js",
                   "js/jquery/1.11.1/jquery.tablesorter.js",
                   "js/jquery/1.11.1/jquery-ui.js",
                   "js/jquery-easing/1.3/jquery.easing.min.js",
                   "js/bootstrap/3.3.2/js/bootstrap.min.js",
                   "js/bootstrap/3.3.2/js/bootstrap.js",
#                            "js/morris/0.5.0/morris.js",
#                            "js/morris/0.5.0/morris.min.js",
                   "js/morris/0.5.0/raphael.min.js",
#                            "js/morris/0.5.0/morris-data.js",
#                            "js/flot/x.x/excanvas.min.js",
#                            "js/flot/x.x/flot-data.js",
#                            "js/flot/x.x/jquery.flot.js",
#                            "js/flot/x.x/jquery.flot.pie.js",
#                            "js/flot/x.x/jquery.flot.resize.js",
#                            "js/flot/x.x/jquery.flot.tooltip.min.js",
                            ]

@login_required(login_url='/landpage')
def course_exams(request, course_id):
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
        'ESSAY_ASSIGNMENT_TYPE' : settings.ESSAY_ASSIGNMENT_TYPE,
        'MULTIPLECHOICE_ASSIGNMENT_TYPE' : settings.MULTIPLECHOICE_ASSIGNMENT_TYPE,
        'TRUEFALSE_ASSIGNMENT_TYPE' : settings.TRUEFALSE_ASSIGNMENT_TYPE,
        'RESPONSE_ASSIGNMENT_TYPE' : settings.RESPONSE_ASSIGNMENT_TYPE,
        'tab' : 'exams',
        'subtab' : '',
        'local_css_urls' : css_library_urls,
        'local_js_urls' : js_library_urls,
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

            if exam_type == settings.MULTIPLECHOICE_ASSIGNMENT_TYPE:
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


@login_required(login_url='/landpage')
def course_discussion(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'course/discussion/discussion.html',{
        'course' : course,
        'user' : request.user,
        'tab' : 'discussion',
        'local_css_urls' : css_library_urls,
        'local_js_urls' : js_library_urls
    })
