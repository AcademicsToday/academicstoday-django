from django.shortcuts import render
from django.core import serializers
from registrar.models import Student
from registrar.models import CoursePreview
from registrar.models import Course
import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#
# (2) JSON
# https://docs.djangoproject.com/en/1.7/topics/serialization/


@login_required(login_url='/landpage')
def courses(request):
    courses = Course.objects.all()
    
    # Create our student account which will build our registration around.
    try:
         student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
         student = Student.objects.create(user=request.user)

    return render(request, 'list.html',{
        'courses' : courses,
        'student' : student,
        'user' : request.user,
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS
    })


@login_required()
def enrol(request):
    response_data = {'status' : 'failure', 'message' : 'unsupported request format'}
    if request.is_ajax():
        course_id = int(request.POST['course_id'])
        student = Student.objects.get(user=request.user)
        course = Course.objects.get(id=course_id)
        
        # Lookup the course in the students enrolment history and if the
        # student is not enrolled, then enrol them now.
        try:
            found_course = Student.objects.get(courses__id=course_id)
        except Student.DoesNotExist:
            student.courses.add(course)
        response_data = {'status' : 'success', 'message' : 'enrolled' }
        
    return HttpResponse(json.dumps(response_data), content_type="application/json")
