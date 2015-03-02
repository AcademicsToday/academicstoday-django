from django.shortcuts import render
from django.core import serializers

from landpage.models import LandpageTeamMember
from landpage.models import LandpageCoursePreview
from landpage.models import CoursePreview

import json
from django.http import HttpResponse

# Create your views here.

# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#
# (2) JSON
# https://docs.djangoproject.com/en/1.7/topics/serialization/


css_library_urls = ["js/jquery/1.11.1/jquery-ui.css",
                    "js/bootstrap/3.3.2/css/bootstrap.min.css",
                    "js/font-awesome/4.2.0/css/font-awesome.css",
                    "js/font-awesome/4.2.0/css/font-awesome.min.css",
                    "css/landpage.css",
                    "css/agency.css"]

js_library_urls = ["js/jquery/1.11.1/jquery.min.js",
                   "js/jquery/1.11.1/jquery.tablesorter.js",
                   "js/jquery/1.11.1/jquery-ui.js",
                   "js/jquery-easing/1.3/jquery.easing.min.js",
                   "js/bootstrap/3.3.2/js/bootstrap.min.js",
                   "js/bootstrap/3.3.2/js/bootstrap.js",
                   "js/classie/1.0.0/classie.js",
                   "js/cbpanimatedheader/1.0.0/cbpAnimatedHeader.js",
                   "js/cbpanimatedheader/1.0.0/cbpAnimatedHeader.min.js",
                   "js/jqbootstrapvalidation/1.3.6/jqBootstrapValidation.js",
                   "js/misc/agency.js"]

def load_landpage(request):
    course_previews = LandpageCoursePreview.objects.all();
    team_members = LandpageTeamMember.objects.all()
    return render(request, 'landpage/main.html',{
        'course_previews' : course_previews,
        'team_members' : team_members,
        'local_css_urls' : css_library_urls,
        'local_js_urls' : js_library_urls
    })


def get_course_preview(request):
    course_preview = None
    if request.method == u'POST':
        POST = request.POST
        preview_course_id = int(POST[u'course_preview_id'])
        course_preview = CoursePreview.objects.get(id=preview_course_id)
    return render(request, 'landpage/course_preview.html',{ 'course_preview' : course_preview })


def get_login(request):
    return render(request, 'landpage/login.html',{})


def get_register(request):
    return render(request, 'landpage/register.html',{})
