from django.shortcuts import render
from django.core import serializers

import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_authentication(request):
    response_data = {}
    if request.is_ajax():
        if request.method == 'POST':
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            
            # Does the user exist for the username and has correct password?
            if user is not None:
                # Is user suspended or active?
                if user.is_active:
                    response_data = {'status' : 'success', 'message' : 'Loging in...'}
                    login(request, user)
                else:
                    response_data = {'status' : 'failure', 'message' : 'You are suspended.'}
            else:
                response_data = {'status' : 'failure', 'message' : 'Wrong username or password.'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def logout_authentication(request):
    response_data = {'status' : 'success', 'message' : 'Done'}
    if request.is_ajax():
        if request.method == 'POST':
            logout(request)
    return HttpResponse(json.dumps(response_data), content_type="application/json")
