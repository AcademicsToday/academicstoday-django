from django.shortcuts import render
from django.core import serializers
from webapp.models import Course
from webapp.models import CourseEnrollment
from webapp.models import Announcement
from webapp.models import Syllabus
from webapp.models import Policy
from webapp.models import Week
from webapp.models import Lecture
import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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

def logout_authentication(request):
    response_data = {'status' : 'success', 'message' : 'Done'}
    if request.is_ajax():
        if request.method == 'POST':
            logout(request)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def course(request, course_id, tab):
    course = Course.objects.get(id=course_id)
    return render(request, 'course/home.html',{
                  'course' : course,
                  'user' : request.user,
                  'tab' : tab,
                  'local_css_urls' : css_library_urls,
                  'local_js_urls' : js_library_urls})


@login_required(login_url='/landpage')
def course_home(request, course_id):
    course = Course.objects.get(id=course_id)
    try:
        announcements = Announcement.objects.filter(course_id=course_id).order_by('-post_date')
    except Announcement.DoesNotExist:
        announcements = None
    return render(request, 'course/home.html',{
                  'course' : course,
                  'announcements' : announcements,
                  'user' : request.user,
                  'tab' : 'home',
                  'local_css_urls' : css_library_urls,
                  'local_js_urls' : js_library_urls})

@login_required(login_url='/landpage')
def course_syllabus(request, course_id):
    course = Course.objects.get(id=course_id)
    try:
        syllabus = Syllabus.objects.get(course_id=course_id)
    except Syllabus.DoesNotExist:
        syllabus = None
    return render(request, 'course/syllabus.html',{
                  'course' : course,
                  'syllabus' : syllabus,
                  'user' : request.user,
                  'tab' : 'syllabus',
                  'local_css_urls' : css_library_urls,
                  'local_js_urls' : js_library_urls})

@login_required(login_url='/landpage')
def course_policy(request, course_id):
    course = Course.objects.get(id=course_id)
    try:
        policy = Policy.objects.get(course_id=course_id)
    except Policy.DoesNotExist:
        policy = None
    return render(request, 'course/policy.html',{
                  'course' : course,
                  'user' : request.user,
                  'policy' : policy,
                  'tab' : 'policy',
                  'local_css_urls' : css_library_urls,
                  'local_js_urls' : js_library_urls})

@login_required(login_url='/landpage')
def course_lectures(request, course_id):
    course = Course.objects.get(id=course_id)
    try:
        weeks = Week.objects.filter(course_id=course_id)
    except Week.DoesNotExist:
        weeks = None
    try:
        lectures = Lecture.objects.filter(course_id=course_id).order_by('-lecture_num')
    except Lecture.DoesNotExist:
        lectures = None
    return render(request, 'course/lectures.html',{
                  'course' : course,
                  'weeks' : weeks,
                  'lectures' : lectures,
                  'user' : request.user,
                  'tab' : 'lectures',
                  'local_css_urls' : css_library_urls,
                  'local_js_urls' : js_library_urls})

@login_required(login_url='/landpage')
def get_lecture(request, course_id):
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
                 return render(request, 'course/lecture.html',{
                                        'lecture' : lecture,
                                        'user' : request.user,
                                        'local_css_urls' : css_library_urls,
                                        'local_js_urls' : js_library_urls})

@login_required(login_url='/landpage')
def course_assignments(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'course/assignments.html',{
                  'course' : course,
                  'user' : request.user,
                  'tab' : 'assignments',
                  'local_css_urls' : css_library_urls,
                  'local_js_urls' : js_library_urls})

@login_required(login_url='/landpage')
def course_quizzes(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'course/quizzes.html',{
                  'course' : course,
                  'user' : request.user,
                  'tab' : 'quizzes',
                  'local_css_urls' : css_library_urls,
                  'local_js_urls' : js_library_urls})

@login_required(login_url='/landpage')
def course_exams(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'course/exams.html',{
                  'course' : course,
                  'user' : request.user,
                  'tab' : 'exams',
                  'local_css_urls' : css_library_urls,
                  'local_js_urls' : js_library_urls})

@login_required(login_url='/landpage')
def course_discussion(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'course/discussion.html',{
                  'course' : course,
                  'user' : request.user,
                  'tab' : 'discussion',
                  'local_css_urls' : css_library_urls,
                  'local_js_urls' : js_library_urls})
