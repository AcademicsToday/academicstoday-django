from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import datetime
from account.models import PrivateMessage
from account.forms import PrivateMessageForm

@login_required(login_url='/landpage')
def mail_page(request):
    try:
        email = request.user.email
        messages = PrivateMessage.objects.filter(to_address=email)
    except PrivateMessage.DoesNotExist:
        messages = None
    
    return render(request, 'account/mail/view.html',{
        'messages': messages,
        'user': request.user,
        'tab': 'inbox',
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


@login_required()
def send_private_message(request):
    response_data = {'status' : 'failed', 'message' : 'unknown error'}
    if request.is_ajax():
        if request.method == 'POST':
            title = request.POST['title']
            text = request.POST['message']
            email = request.POST['email']
            
            # Validate email exists on system.
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                response_data = {'status' : 'failure', 'message' : 'email does not exist in our system'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")

            PrivateMessage.objects.create(
                title=title,
                text=text,
                to_address=email,
                from_address=request.user.email,
            ).save()

            response_data = {'status' : 'success', 'message' : 'private message sent'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def view_private_message(request):
    response_data = {'status' : 'failed', 'message' : 'unknown error'}
    if request.is_ajax():
        if request.method == 'POST':
            message_id = int(request.POST['message_id'])
            try:
                message = PrivateMessage.objects.get(id=message_id)
            except PrivateMessage.DoesNotExist:
                message = None
            
            form = PrivateMessageForm(instance=message)
            return render(request, 'account/mail/modal.html',{
                'form': form,
                'user': request.user,
                'tab': 'inbox',
                'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
                'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS,
            })


@login_required()
def delete_private_message(request):
    response_data = {'status' : 'failed', 'message' : 'unknown error'}
    if request.is_ajax():
        if request.method == 'POST':
            message_id = int(request.POST['message_id'])
            try:
                message = PrivateMessage.objects.get(
                    id=message_id,
                ).delete()
            except PrivateMessage.DoesNotExist:
                message = None
            
            response_data = {'status' : 'success', 'message' : 'deleted private message'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")