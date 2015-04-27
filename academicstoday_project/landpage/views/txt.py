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


def robots_txt_page(request):
    return render(request, 'misc/robots.txt', {}, content_type="text/plain")


def humans_txt_page(request):
    return render(request, 'misc/humans.txt', {}, content_type="text/plain")


def terms_txt_page(request):
    return render(request, 'misc/terms.txt', {}, content_type="text/plain")


def privacy_txt_page(request):
    return render(request, 'misc/privacy.txt', {}, content_type="text/plain")