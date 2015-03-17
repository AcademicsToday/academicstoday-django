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
from registrar.models import Student
from registrar.models import CourseDiscussionPost
from registrar.models import CourseDiscussionThread
from student.forms import CourseDiscussionThreadForm

@login_required(login_url='/landpage')
def discussion_page(request, course_id):
    course = Course.objects.get(id=course_id)
    
    try:
        threads = CourseDiscussionThread.objects.filter(course=course).order_by('date')
    except:
        threads = None
    
    return render(request, 'course/discussion/threads_list.html',{
        'course': course,
        'threads': threads,
        'user': request.user,
        'tab': 'discussion',
        'local_css_urls': settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def new_thread_modal(request, course_id):
    course = Course.objects.get(id=course_id)
    form = CourseDiscussionThreadForm()
    return render(request, 'course/discussion/new_thread_modal.html',{
        'course': course,
        'form': form,
        'user': request.user,
        'tab': 'discussion',
        'local_css_urls': settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_JS_LIBRARY_URLS,
    })

@login_required(login_url='/landpage')
def insert_thread(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error detected.'}
    if request.is_ajax():
        if request.method == 'POST':
            course = Course.objects.get(id=course_id)
            form = CourseDiscussionThreadForm(request.POST)
            form.instance.user = request.user
            if form.is_valid():
                form.save()
                response_data = {'status' : 'success', 'message' : 'submitted'}
            else:
                response_data = {'status' : 'failed', 'message' : form.errors}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
