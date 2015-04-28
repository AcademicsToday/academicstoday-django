from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import datetime
from registrar.models import Teacher
from registrar.models import Course
from registrar.models import Policy
from teacher.forms import PolicyForm

@login_required(login_url='/landpage')
def policy_page(request, course_id):
    course = Course.objects.get(id=course_id)
    try:
        policy = Policy.objects.get(course=course)
    except Policy.DoesNotExist:
        policy = None
    return render(request, 'teacher/policy/view.html',{
        'course' : course,
        'policy' : policy,
        'user' : request.user,
        'tab' : 'policy',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })

@login_required(login_url='/landpage')
def policy_modal(request, course_id):
    if request.method == u'POST':
        form = PolicyForm()
        return render(request, 'teacher/policy/modal.html',{'form' : form })


@login_required(login_url='/landpage')
def save_policy(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            form = PolicyForm(request.POST, request.FILES)
            if form.is_valid():
                course = Course.objects.get(id=course_id)
                form.instance.course = course
                form.save()
                response_data = {'status' : 'success', 'message' : 'saved'}
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def delete_policy(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deleting'}
    if request.is_ajax():
        if request.method == 'POST':
            policy_id = int(request.POST['policy_id'])
            teacher = Teacher.objects.get(user=request.user)
            try:
                policy = Policy.objects.get(policy_id=policy_id)
                if policy.course.teacher == teacher:
                    policy.delete()
                    response_data = {'status' : 'success', 'message' : 'deleted'}
                else:
                    response_data = {'status' : 'failed', 'message' : 'unauthorized deletion'}
            except Policy.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'record does not exist'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

