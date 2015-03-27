from django.shortcuts import render
from django.core import serializers
import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from landpage.models import CoursePreview
from registrar.models import Student
from registrar.models import Teacher
from registrar.models import Course
from registrar.models import CourseFinalMark
from registrar.models import CourseSetting
from registrar.forms import CourseForm


@login_required(login_url='/landpage')
def courses_page(request):
    courses = Course.objects.filter(status=settings.COURSE_AVAILABLE_STATUS)

    # Create our student account which will build our registration around.
    try:
         student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
         student = Student.objects.create(user=request.user)

    # Only fetch teacher and do not create new teacher here.
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        teacher = None

    return render(request, 'registrar/courses/list.html',{
        'courses' : courses,
        'student' : student,
        'teacher' : teacher,
        'user' : request.user,
        'tab' : 'courses',
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