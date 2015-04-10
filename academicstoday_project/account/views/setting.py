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
def settings_page(request):
    return render(request, 'account/settings/view.html',{
        'user' : request.user,
        'tab' : 'settings',
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


@login_required()
def update_password(request):
    response_data = {'status' : 'failed', 'message' : 'unknown deletion error'}
    if request.is_ajax():
        if request.method == 'POST':
            old_password = request.POST['old_password']
            password = request.POST['password']
            repeat_password = request.POST['repeat_password']
            
            # Validate password.
            if request.user.check_password(old_password) == False:
                response_data = {'status' : 'failure', 'message' : 'invalid old password' }
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            if password is '' or request is '':
                response_data = {'status' : 'failure', 'message' : 'blank passwords are not acceptable' }
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            if password != repeat_password:
                response_data = {'status' : 'failure', 'message' : 'passwords do not match' }
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        
            # Update model
            request.user.set_password(password)
            request.user.save()

            response_data = {'status' : 'success', 'message' : 'updated password'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")