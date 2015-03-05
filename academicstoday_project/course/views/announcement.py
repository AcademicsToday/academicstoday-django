from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from registrar.models import Course
from course.models import Announcement
import json
import datetime

# Forms
from course.forms import EssaySubmissionForm
from course.forms import AssignmentSubmissionForm


# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#
# (2) JSON
# https://docs.djangoproject.com/en/1.7/topics/serialization/

@login_required(login_url='/landpage')
def announcements_page(request, course_id):
    course = Course.objects.get(id=course_id)
    try:
        announcements = Announcement.objects.filter(course_id=course_id).order_by('-post_date')
    except Announcement.DoesNotExist:
        announcements = None
    return render(request, 'announcement/list.html',{
        'course' : course,
        'announcements' : announcements,
        'user' : request.user,
        'tab' : 'home',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
    })
