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
    try:
        courses = Course.objects.filter(teacher=teacher)
    except Course.DoesNotExist:
        courses = None

    return render(request, 'registrar/teaching/view.html',{
        'teacher' : teacher,
        'courses': courses,
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
    try:
        courses = Course.objects.filter(teacher=teacher)
    except Course.DoesNotExist:
        courses = None

    return render(request, 'registrar/teaching/table.html',{
        'teacher' : teacher,
        'courses': courses,
        'user' : request.user,
        'tab' : 'teaching',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS
    })


@login_required(login_url='/landpage')
def course_modal(request):
    if request.method == u'POST':
        course_id = int(request.POST['course_id'])
        form = None
        course = None
        if course_id > 0:
            course = Course.objects.get(id=course_id)
            form = CourseForm(instance=course)
        else:
            form = CourseForm()
        return render(request, 'registrar/teaching/new_course_modal.html',{
            'course': course,
            'course_form' : form,
        })

@login_required()
def delete_course_modal(request):
    course = None
    if request.is_ajax():
        if request.method == 'POST':
            course_id = int(request.POST['course_id'])
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                course = None
    return render(request, 'registrar/teaching/delete_course_modal.html',{
        'course' : course,
    })


@login_required(login_url='/landpage')
def save_course(request):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            course_id = int(request.POST['course_id'])
            form = None
            
            if course_id > 0:
                try:
                    course = Course.objects.get(id=course_id)
                    form = CourseForm(instance=course, data=request.POST)
                except Announcement.DoesNotExist:
                    return HttpResponse(json.dumps({
                        'status' : 'failed', 'message' : 'cannot find record'
                    }), content_type="application/json")
            else:
                try:
                    teacher = Teacher.objects.get(user=request.user)
                except Teacher.DoesNotExist:
                    teacher = Teacher.objects.create(user=request.user)
                
                form = CourseForm(request.POST, request.FILES)
                form.instance.teacher = teacher
            
            if form.is_valid():
                form.save()
                response_data = {'status' : 'success', 'message' : 'saved'}
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
