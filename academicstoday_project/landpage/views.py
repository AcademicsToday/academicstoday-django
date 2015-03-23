from django.shortcuts import render
from django.core import serializers

from landpage.models import LandpageTeamMember
from landpage.models import LandpageCoursePreview
from landpage.models import CoursePreview
from landpage.models import LandpageContactMessage

import json
from django.http import HttpResponse
from django.conf import settings

# Create your views here.

# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#
# (2) JSON
# https://docs.djangoproject.com/en/1.7/topics/serialization/


def robots_txt_page(request):
    return render(request, 'misc/robots.txt', {}, content_type="text/plain")


def humans_txt_page(request):
    return render(request, 'misc/humans.txt', {}, content_type="text/plain")


def landpage_page(request):
    course_previews = LandpageCoursePreview.objects.all();
    team_members = LandpageTeamMember.objects.all()
    return render(request, 'landpage/main.html',{
        'course_previews' : course_previews,
        'team_members' : team_members,
        'local_css_urls' : settings.AGENCY_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.AGENCY_JS_LIBRARY_URLS
    })


def course_preview_modal(request):
    course_preview = None
    if request.method == u'POST':
        POST = request.POST
        value = POST.get('course_preview_id')
        if value is not None:
            preview_course_id = int(value)
            try:
                course_preview = CoursePreview.objects.get(id=preview_course_id)
            except CoursePreview.DoesNotExist:
                pass
    return render(request, 'landpage/course_preview.html',{ 'course_preview' : course_preview })


def login_modal(request):
    return render(request, 'landpage/login.html',{})


def register_modal(request):
    return render(request, 'landpage/register.html',{})


def terms_txt_page(request):
    return render(request, 'misc/terms.txt', {}, content_type="text/plain")


def privacy_txt_page(request):
    return render(request, 'misc/privacy.txt', {}, content_type="text/plain")


def save_contact_us_message(request):
    response_data = {'status' : 'failed', 'message' : 'unknown error with sending message'}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                name = request.POST['name']
                email = request.POST['email']
                phone = request.POST['phone']
                message = request.POST['message']
                
                LandpageContactMessage.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    message=message,
                ).save()
                
                response_data = {'status' : 'success', 'message' : 'saved'}
            except:
                response_data = {
                    'status' : 'failure',
                    'message' : 'could not save message ' + name + ' ' + email + ' ' + phone + ' ' + message
                }
    return HttpResponse(json.dumps(response_data), content_type="application/json")
