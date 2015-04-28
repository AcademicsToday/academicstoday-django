from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import datetime
from registrar.models import Student
from registrar.models import Course
from registrar.models import Announcement


@login_required(login_url='/landpage')
def announcements_page(request, course_id):
    course = Course.objects.get(id=course_id)
    try:
        announcements = Announcement.objects.filter(course=course).order_by('-post_date')
    except Announcement.DoesNotExist:
        announcements = None
    return render(request, 'course/announcement/view.html',{
        'course' : course,
        'announcements' : announcements,
        'user' : request.user,
        'tab' : 'announcements',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })
