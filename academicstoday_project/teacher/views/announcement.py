from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import datetime
from registrar.models import Teacher
from registrar.models import Student
from registrar.models import Course
from registrar.models import Announcement
from teacher.forms import AnnouncementForm

# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#


@login_required(login_url='/landpage')
def announcements_page(request, course_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)

    try:
        announcements = Announcement.objects.filter(course=course).order_by('-post_date')
    except Announcement.DoesNotExist:
        announcements = None
    return render(request, 'teacher/announcement/list.html',{
        'teacher' : teacher,
        'course' : course,
        'announcements' : announcements,
        'user' : request.user,
        'tab' : 'home',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
    })

@login_required(login_url='/landpage')
def new_announcement_modal(request, course_id):
    if request.method == u'POST':
        form = AnnouncementForm()
        return render(request, 'teacher/announcement/new_modal.html',{
            'form' : form,
        })


@login_required(login_url='/landpage')
def save_new_announcement(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            form = AnnouncementForm(request.POST, request.FILES)
            if form.is_valid():
                course = Course.objects.get(id=course_id)
                form.instance.course = course
                form.save()
                response_data = {'status' : 'success', 'message' : 'unknown error with saving'}
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def announcement_delete(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deleting'}
    if request.is_ajax():
        if request.method == 'POST':
            announcement_id = int(request.POST['announcement_id'])
            announcement = Announcement.objects.get(announcement_id=announcement_id)
            announcement.delete()
            response_data = {'status' : 'success', 'message' : 'deleted'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
