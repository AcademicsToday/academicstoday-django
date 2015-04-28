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
    
    return render(request, 'teacher/announcement/view.html',{
        'teacher' : teacher,
        'course' : course,
        'announcements' : announcements,
        'user' : request.user,
        'tab' : 'home',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def announcements_table(request, course_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)
    
    try:
        announcements = Announcement.objects.filter(course=course).order_by('-post_date')
    except Announcement.DoesNotExist:
        announcements = None
    return render(request, 'teacher/announcement/table.html',{
        'teacher' : teacher,
        'course' : course,
        'announcements' : announcements,
        'user' : request.user,
    })


@login_required(login_url='/landpage')
def announcement_modal(request, course_id):
    if request.method == u'POST':
        # Get the announcement_id of post and either create a brand new form
        # for the user, or load up existing one based on the database
        # data for the particular assignment.
        announcement_id = int(request.POST['announcement_id'])
        form = None
        if announcement_id > 0:
            announcement = Announcement.objects.get(announcement_id=announcement_id)
            form = AnnouncementForm(instance=announcement)
        else:
            form = AnnouncementForm()
        return render(request, 'teacher/announcement/modal.html',{'form' : form})


@login_required(login_url='/landpage')
def save_announcement(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            course = Course.objects.get(id=course_id)
            announcement_id = int(request.POST['announcement_id'])
            form = None
            # If announcement already exists, then lets update only, else insert.
            if announcement_id > 0:
                try:
                    announcement = Announcement.objects.get(announcement_id=announcement_id)
                except Announcement.DoesNotExist:
                    return HttpResponse(json.dumps({
                        'status' : 'failed', 'message' : 'cannot find record'
                    }), content_type="application/json")
                form = AnnouncementForm(instance=announcement, data=request.POST)
            else:
                form = AnnouncementForm(request.POST, request.FILES)
                form.instance.course = course
            
            if form.is_valid():
                form.save()
                response_data = {'status' : 'success', 'message' : 'saved'}
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def delete_announcement(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deleting'}
    if request.is_ajax():
        if request.method == 'POST':
            announcement_id = int(request.POST['announcement_id'])
            teacher = Teacher.objects.get(user=request.user)
            try:
                announcement = Announcement.objects.get(announcement_id=announcement_id)
                if announcement.course.teacher == teacher:
                    announcement.delete()
                    response_data = {'status' : 'success', 'message' : 'deleted'}
                else:
                    response_data = {'status' : 'failed', 'message' : 'unauthorized deletion'}
            except Announcement.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'cannot find record'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
