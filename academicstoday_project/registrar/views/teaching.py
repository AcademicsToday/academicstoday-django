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
def teaching_page(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        teacher = None

    return render(request, 'registrar/teaching/view.html',{
        'teacher' : teacher,
        'user' : request.user,
        'tab' : 'teaching',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS
    })


@login_required(login_url='/landpage')
def refresh_teaching_table(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        teacher = None
    
    return render(request, 'registrar/teaching/table.html',{
        'teacher' : teacher,
        'user' : request.user,
        'tab' : 'teaching',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS
    })


@login_required(login_url='/landpage')
def new_course_modal(request):
    if request.method == u'POST':
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            course_form.save()
    else:
        course_form = CourseForm()

    return render(request, 'registrar/teaching/new_course_modal.html',{
        'course_form' : course_form,
    })


@login_required(login_url='/landpage')
def save_new_course(request):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()  # Save course to the database.
                
                # Course Initialization
                CourseSetting.objects.create(
                    course=form.instance
                ).save()
                
                # Create our teacher account which will build our course around.
                try:
                    teacher = Teacher.objects.get(user=request.user)
                except Teacher.DoesNotExist:
                    teacher = Teacher.objects.create(user=request.user)
                teacher.courses.add(form.instance)
                response_data = {'status' : 'success', 'message' : 'unknown error with saving'}
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def course_delete(request):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deleting'}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                course_id = int(request.POST['course_id'])
                teacher = Teacher.objects.get(user=request.user)
                course = Course.objects.get(id=course_id)
                course.delete()
                response_data = {'status' : 'success', 'message' : 'deleted'}
            except Teacher.DoesNotExist:
                response_data = {'status' : 'failure', 'message' : 'no teacher'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
