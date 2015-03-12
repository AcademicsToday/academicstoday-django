from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import datetime
from registrar.models import Course
from registrar.models import Student
from registrar.models import Assignment
from registrar.models import AssignmentSubmission
from registrar.models import EssayQuestion
from registrar.models import EssaySubmission
from registrar.models import EssaySubmissionReview
from registrar.models import ResponseQuestion
from registrar.models import ResponseSubmission

# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#
# (2) JSON
# https://docs.djangoproject.com/en/1.7/topics/serialization/

@login_required(login_url='/landpage')
def peer_review_page(request, course_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user)
    
    # Fetch all the assignments for this course.
    try:
        assignments = Assignment.objects.filter(course=course).order_by('assignment_num')
    except Assignment.DoesNotExist:
        assignments = None
    
    # Fetch all submitted assignments
    try:
        submissions = AssignmentSubmission.objects.filter(course=course)
    except AssignmentSubmission.DoesNotExist:
        submissions = None

    return render(request, 'course/peer_review/assignments_list.html',{
        'course' : course,
        'assignments': assignments,
        'submissions': submissions,
        'user' : request.user,
        'tab' : 'peer_reviews',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def assignment_page(request, course_id, assignment_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user)
    assignment = Assignment.objects.get(assignment_id=assignment_id)
    
    # Load all essay type questions for this assignment.
    try:
        e_submissions = EssaySubmission.objects.filter(assignment=assignment)
    except EssayQuestion.DoesNotExist:
        e_submissions = None
    try:
        e_reviews = EssaySubmissionReview.objects.filter(assignment=assignment)
    except EssaySubmissionReview.DoesNotExist:
        e_reviews = None

    # Load all response type questions for this assignment.
    try:
        r_submissions = ResponseSubmission.objects.filter(assignment=assignment)
    except ResponseQuestion.DoesNotExist:
        r_submissions = None
    
    return render(request, 'course/peer_review/question_list.html',{
        'student': student,
        'course': course,
        'assignment': assignment,
        'e_submissions': e_submissions,
        'e_reviews': e_reviews,
        'r_submissions': r_submissions,
        'ESSAY_QUESTION_TYPE': settings.ESSAY_QUESTION_TYPE,
        'MULTIPLECHOICE_QUESTION_TYPE': settings.MULTIPLECHOICE_QUESTION_TYPE,
        'TRUEFALSE_QUESTION_TYPE': settings.TRUEFALSE_QUESTION_TYPE,
        'RESPONSE_QUESTION_TYPE': settings.RESPONSE_QUESTION_TYPE,
        'user': request.user,
        'tab': 'peer_review',
        'local_css_urls': settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_JS_LIBRARY_URLS,
    })

