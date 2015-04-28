import json
import random, string
from django.shortcuts import render
from django.core import serializers
from landpage.form import ForgotPasswordForm
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail

def forgot_password_page(request):
    form = ForgotPasswordForm()
    return render(request, 'offlandpage/page/forgot_password.html',{
        'form': form,
        'tab': 'forget_password',
        'local_css_urls': ["css/offlandpage.css",
                            "bower_components/bootstrap/dist/css/bootstrap.min.css"],
        'local_js_urls': ["bower_components/jquery/dist/jquery.min.js",
                           "bower_components/bootstrap/dist/js/bootstrap.min.js",],
    })


def reset_password(request):
    response_data = {'status' : 'failure', 'message' : 'unknown error occured' }
    if request.is_ajax():
        if request.method == 'POST':
            form = ForgotPasswordForm(request.POST)
            # Validate the form: the captcha field will automatically
            # check the input
            if form.is_valid():
                # Get the email and then create a random password for the client
                # and send the client the new password to their email address.
                email = request.POST['email']
                new_password = create_random_password(email)
                response_data = send_email(email, new_password)
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def random_word(length):
    return ''.join(random.choice("abcdefghijklmnopqrstuvwxyz123467890") for i in range(length))


def create_random_password(email):
    # Create new password
    new_password = random_word(8)
    
    # Update the user account
    user = User.objects.get(email=email)
    user.set_password(new_password)
    user.save()
    
    # Return the new password
    return new_password


def send_email(email, new_password):
    if settings.EMAIL_HOST_USER is '' or settings.EMAIL_HOST_PASSWORD is '':
        return {'status' : 'failed', 'message' : 'cannot change password, emailer is offline, please check back later' }
    
    text = "Your new password is: " + new_password
            
    send_mail(
        "New Password",
        text,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )
    return {'status' : 'success', 'message' : 'successfully registered' }