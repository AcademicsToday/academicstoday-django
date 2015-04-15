from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from landpage.form import RegisterForm

def register(request):
    response_data = {}
    if request.is_ajax():
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            # Validate the form: the captcha field will automatically
            # check the input
            if form.is_valid():
                response_data = {'status' : 'success', 'message' : 'successfully registered' }
                
                # Check to see if we already have the username or email taken.
                try:
                    user = User.objects.get(email__exact=request.POST['electronic_mail'])
                    response_data = {'status' : 'failure', 'message' : 'Email already exists, please choose another email' }
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
                except User.DoesNotExist:
                    pass
                
                # Create the user in our database
                try:
                    user = User.objects.create_user(
                        request.POST['electronic_mail'],  # Username
                        request.POST['electronic_mail'],
                        request.POST['password']
                    )
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.save()
                    response_data = {'status' : 'success', 'message' : 'successfully registered' }
                except Exception as e:
                    response_data = {'status' : 'failure', 'message' : 'An unknown error occured, failed registering.' }
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    else:
        response_data = {'status' : 'failure', 'message' : 'Not acceptable request made.' }
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")
