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
from student.forms import CourseDiscussionPostForm


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
            form.instance.course = course
            if form.is_valid():
                form.save()
                response_data = {'status' : 'success', 'message' : 'submitted'}
            else:
                response_data = {'status' : 'failed', 'message' : form.errors}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def delete_thread(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deletion'}
    if request.is_ajax():
        if request.method == 'POST':
            thread_id = int(request.POST['thread_id'])
            course = Course.objects.get(id=course_id)
            try:
                thread = CourseDiscussionThread.objects.get(
                    course=course,
                    thread_id=thread_id
                ).delete()
                response_data = {'status' : 'success', 'message' : 'deleted record'}
            except CourseDiscussionThread.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'record does not exist'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def thread_page(request, course_id, thread_id):
    course = Course.objects.get(id=course_id)
    
    try:
        thread = CourseDiscussionThread.objects.get(
            course=course,
            thread_id=thread_id
        )
    except CourseDiscussionThread.DoesNotExist:
        thread = None

    return render(request, 'course/discussion/thread_page.html',{
        'course': course,
        'thread': thread,
        'user': request.user,
        'tab': 'thread',
        'local_css_urls': settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def new_post_modal(request, course_id, thread_id):
    course = Course.objects.get(id=course_id)
    thread = CourseDiscussionThread.objects.get(
        course=course,
        thread_id=thread_id
    )
    form = CourseDiscussionPostForm()
    return render(request, 'course/discussion/new_post_modal.html',{
        'course': course,
        'form': form,
        'thread': thread,
        'user': request.user,
        'tab': 'discussion',
        'local_css_urls': settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def insert_post(request, course_id, thread_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error detected.'}
    if request.is_ajax():
        if request.method == 'POST':
            course = Course.objects.get(id=course_id)
            thread = CourseDiscussionThread.objects.get(
                course=course,
                thread_id=thread_id
            )
            form = CourseDiscussionPostForm(request.POST)
            form.instance.user = request.user
            form.instance.course = course
            if form.is_valid():
                form.save()
                thread.posts.add(form.instance)
                response_data = {'status' : 'success', 'message' : 'submitted'}
            else:
                response_data = {'status' : 'failed', 'message' : form.errors}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
