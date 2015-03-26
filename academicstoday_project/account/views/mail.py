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
def inbox_page(request):
    return render(request, 'account/mail/view.html',{
        'user' : request.user,
        'tab' : 'inbox',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
    })
