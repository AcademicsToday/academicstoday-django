from django.shortcuts import render
from django.core import serializers

import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def register(request):
    response_data = {}
    if request.is_ajax():
        if request.method == 'POST':
            # Check to see if any fields where missing from the form.
            if request.POST['first_name'] == '':
                response_data = {'status' : 'failure', 'message' : 'Missing first name.' }
            elif request.POST['last_name'] == '':
                response_data = {'status' : 'failure', 'message' : 'Missing last name.' }
            elif request.POST.get('email') == '':
                response_data = {'status' : 'failure', 'message' : 'Missing email.' }
            elif request.POST['password'] == '':
                response_data = {'status' : 'failure', 'message' : 'Missing password.' }
            elif request.POST['password_repeated'] == '':
                response_data = {'status' : 'failure', 'message' : 'Missing password repeated again.' }
            elif request.POST['is_18_or_plus'] == 'false':
                response_data = {'status' : 'failure', 'message' : 'You must be 18 or over.' }
            elif request.POST['password'] != request.POST['password_repeated']:
                response_data = {'status' : 'failure', 'message' : 'Passwords do not match.' }
            else:
                # Check to see if we already have the username or email taken.
                try:
                    user = User.objects.get(email__exact=request.POST['email'])
                    response_data = {'status' : 'failure', 'message' : 'Email already exists, please choose another email' }
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
                except User.DoesNotExist:
                    pass
                
                # Create the user in our database
                try:
                    user = User.objects.create_user(request.POST['email'], request.POST['email'], request.POST['password'])
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.save()
                    response_data = {'status' : 'success', 'message' : 'successfully registered' }
                except Exception as e:
                    response_data = {'status' : 'failure', 'message' : 'An unknown error occured, failed registering.' }
    else:
        response_data = {'status' : 'failure', 'message' : 'Not acceptable request made.' }
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")
