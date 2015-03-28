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
def profile_page(request):
    return render(request, 'account/profile/view.html',{
        'user' : request.user,
        'tab' : 'profile',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
    })


@login_required()
def update_user(request):
    response_data = {'status' : 'failed', 'message' : 'unknown deletion error'}
    if request.is_ajax():
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            
            # Validate email.
            # Check to see if we already have the username or email taken.
            try:
                user = User.objects.get(email__exact=request.POST['email'])
                if user != request.user:
                    response_data = {'status' : 'failure', 'message' : 'Email already exists, please choose another email' }
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
            except User.DoesNotExist:
                user = request.user

            # Update model
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = email
            user.save()

            response_data = {'status' : 'success', 'message' : 'updated user'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
