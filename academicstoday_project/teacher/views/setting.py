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

@login_required(login_url='/landpage')
def settings_page(request, course_id):
    course = Course.objects.get(id=course_id)

    return render(request, 'teacher/setting/view.html',{
        'course': course,
        'COURSE_SUBMITTED_FOR_REVIEW_STATUS': settings.COURSE_SUBMITTED_FOR_REVIEW_STATUS,
        'COURSE_IN_REVIEW_STATUS': settings.COURSE_IN_REVIEW_STATUS,
        'COURSE_UNAVAILABLE_STATUS': settings.COURSE_UNAVAILABLE_STATUS,
        'COURSE_AVAILABLE_STATUS': settings.COURSE_AVAILABLE_STATUS,
        'COURSE_REJECTED_STATUS': settings.COURSE_REJECTED_STATUS,
        'user': request.user,
        'tab': 'settings',
        'local_css_urls': settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_JS_LIBRARY_URLS,
    })
