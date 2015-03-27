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
def enrolment_page(request):
    # Create our student account which will build our registration around.
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = Student.objects.create(user=request.user)
    return render(request, 'registrar/enrolment/list.html',{
        'student' : student,
        'user' : request.user,
        'tab' : 'enrolment',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS
    })