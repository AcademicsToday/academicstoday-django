from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import datetime
from registrar.models import Course
from registrar.models import Syllabus
from teacher.forms import SyllabusForm

@login_required(login_url='/landpage')
def syllabus_page(request, course_id):
    course = Course.objects.get(id=course_id)
    try:
        syllabus = Syllabus.objects.get(course=course)
    except Syllabus.DoesNotExist:
        syllabus = None
    return render(request, 'teacher/syllabus/view.html',{
        'course' : course,
        'syllabus' : syllabus,
        'user' : request.user,
        'tab' : 'syllabus',
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })

@login_required(login_url='/landpage')
def syllabus_modal(request, course_id):
    if request.method == u'POST':
        form = SyllabusForm()
        return render(request, 'teacher/syllabus/modal.html',{'form' : form })


@login_required(login_url='/landpage')
def save_syllabus(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            form = SyllabusForm(request.POST, request.FILES)
            if form.is_valid():
                course = Course.objects.get(id=course_id)
                form.instance.course = course
                form.save()
                response_data = {'status' : 'success', 'message' : 'saved'}
            else:
                response_data = {'status' : 'failed', 'message' : 'could not save.'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def delete_syllabus(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deleting'}
    if request.is_ajax():
        if request.method == 'POST':
            syllabus_id = int(request.POST['syllabus_id'])
            try:
                Syllabus.objects.get(syllabus_id=syllabus_id).delete()
                response_data = {'status' : 'success', 'message' : 'deleted'}
            except Syllabus.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'record does not exist'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

