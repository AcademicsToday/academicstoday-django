import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from registration.form import RegisterForm


def register_modal(request):
    form = RegisterForm()
    return render(request, 'register/modal.html',{
        'form': form,
    })


def register(request):
    response_data = {}
    if request.is_ajax():
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            # Validate the form: the captcha field will automatically
            # check the input
            if form.is_valid():
                response_data = create_user(form)  # Create our store
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    else:
        response_data = {'status' : 'failure', 'message' : 'Not acceptable request made.' }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def create_user(form):
    # Create the user in our database
    email = form['email'].value().lower()
    try:
        user = User.objects.create_user(
            email,  # Username
            email,  # Email
            form['password'].value(),
        )
        user.first_name = form['first_name'].value()
        user.last_name = form['last_name'].value()
        # user.is_active = False;  # Need email verification to change status.
        user.save()
    except Exception as e:
        return {
            'status' : 'failure',
            'message' : 'An unknown error occured, failed registering user.'
    }

    # Return success status
    return {
        'status' : 'success',
        'message' : 'user registered'
    }
