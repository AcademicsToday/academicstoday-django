from django.shortcuts import render
from django.core import serializers

from landpage.models import LandpageTeamMember
from landpage.models import LandpageTopPickCourse
from landpage.models import LandpageCoursePreview
from landpage.models import CoursePreview
from landpage.models import LandpageContactMessage
from landpage.models import LandpagePartner
from registrar.models import Course
from landpage.form import RegisterForm

import json
from django.http import HttpResponse
from django.conf import settings


def privacy_page(request):
    return render(request, 'offlandpage/page/privacy.html',{
        'tab': 'privacy',
        'local_css_urls': ["css/offlandpage.css",
                            "bower_components/bootstrap/dist/css/bootstrap.min.css"],
        'local_js_urls': ["bower_components/jquery/dist/jquery.min.js",
                           "bower_components/bootstrap/dist/js/bootstrap.min.js",],
    })
