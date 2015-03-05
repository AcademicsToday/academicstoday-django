from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from course.models import Course
from course.models import Week
from course.models import Lecture
import json
import datetime



# Forms
from course.forms import EssaySubmissionForm
from course.forms import AssignmentSubmissionForm


# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#
# (2) JSON
# https://docs.djangoproject.com/en/1.7/topics/serialization/


@login_required(login_url='/landpage')
def lectures_page(request, course_id):
    course = Course.objects.get(id=course_id)
    try:
        weeks = Week.objects.filter(course_id=course_id)
    except Week.DoesNotExist:
        weeks = None
    try:
        lectures = Lecture.objects.filter(course_id=course_id).order_by('-lecture_num')
    except Lecture.DoesNotExist:
        lectures = None
    return render(request, 'course/lecture/list.html',{
        'course' : course,
        'weeks' : weeks,
        'lectures' : lectures,
        'user' : request.user,
        'tab' : 'lectures',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def lecture(request, course_id):
    response_data = {}
    if request.is_ajax():
         if request.method == 'POST':
             # Check to see if any fields where missing from the form.
             if request.POST['lecture_id'] != '':
                 try:
                     lecture_id = request.POST['lecture_id']
                     lecture = Lecture.objects.get(id=lecture_id)
                 except Lecture.DoesNotExist:
                     lecture = None
                 return render(request, 'course/lecture/details.html',{
                    'lecture' : lecture,
                    'user' : request.user,
                    'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
                    'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
                 })
