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
def enrolment_page(request):
    # Create our student account which will build our registration around.
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = Student.objects.create(user=request.user)
    try:
        courses = Course.objects.filter(students__student_id=student.student_id)
    except Course.DoesNotExist:
        courses = None
    return render(request, 'registrar/enrolment/view.html',{
        'student' : student,
        'courses': courses,
        'user' : request.user,
        'tab' : 'enrolment',
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS
    })


@login_required()
def enrolment_table(request):
    # Create our student account which will build our registration around.
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = Student.objects.create(user=request.user)
    try:
        courses = Course.objects.filter(students__student_id=student.student_id)
    except Course.DoesNotExist:
        courses = None
    return render(request, 'registrar/enrolment/table.html',{
        'student' : student,
        'courses': courses,
        'user' : request.user,
        'tab' : 'enrolment',
    })

@login_required()
def disenroll_modal(request):
    # Create our student account which will build our registration around.
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = Student.objects.create(user=request.user)

    course_id = int(request.POST['course_id'])
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        course = None
    return render(request, 'registrar/enrolment/disenroll_modal.html',{
        'student' : student,
        'course': course,
        'user' : request.user,
        'tab' : 'enrolment',
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS
    })


@login_required()
def disenrol(request):
    response_data = {'status' : 'failure', 'message' : 'unsupported request format'}
    if request.is_ajax():
        course_id = int(request.POST['course_id'])
        student = Student.objects.get(user=request.user)
        course = Course.objects.get(id=course_id)
        course.students.remove(student)
        response_data = {'status' : 'success', 'message' : 'disenroled' }
    return HttpResponse(json.dumps(response_data), content_type="application/json")




