from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from registrar.models import Course
from course.models import Assignment
from course.models import AssignmentSubmission
from course.models import AssignmentReview
from course.models import EssayQuestion
from course.models import EssaySubmission
from course.models import ResponseQuestion
from course.models import ResponseSubmission
import json
import datetime

# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#
# (2) JSON
# https://docs.djangoproject.com/en/1.7/topics/serialization/

@login_required(login_url='/landpage')
def peer_review_page(request, course_id):
    course = Course.objects.get(id=course_id)

    try:
        assignments = Assignment.objects.filter(course_id=course_id).order_by('-order_num')
    except Assignment.DoesNotExist:
        assignments = None

    try:
        submissions = AssignmentSubmission.objects.filter(course_id=course_id).order_by('-order_num')
    except AssignmentSubmission.DoesNotExist:
        announcements = None

    try:
        essay_questions = EssayQuestion.objects.filter(course_id=course_id).order_by('-order_num')
    except EssayQuestion.DoesNotExist:
        essay_questions = None

    try:
        essay_submissions = EssaySubmission.objects.filter(course_id=course_id).order_by('-order_num')
    except EssaySubmission.DoesNotExist:
        essay_submissions = None

    try:
        mc_questions = ResponseQuestion.objects.filter(course_id=course_id).order_by('-order_num')
    except ResponseQuestion.DoesNotExist:
        mc_questions = None

    try:
        mc_submissions = ResponseSubmission.objects.filter(course_id=course_id).order_by('-order_num')
    except ResponseSubmission.DoesNotExist:
        mc_submissions = None

    try:
        reviews = AssignmentReview.objects.filter(course_id=course_id).order_by('-order_num')
    except AssignmentReview.DoesNotExist:
        reviews = None

    return render(request, 'course/peer_review/list.html',{
        'course' : course,
        'assignments' : assignments,
        'submissions' : submissions,
        'essay_questions' : essay_questions,
        'essay_submissions' : essay_submissions,
        'mc_questions' : mc_questions,
        'mc_submissions' : mc_submissions,
        'reviews' : reviews,
        'user' : request.user,
        'tab' : 'peer_review',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
    })
