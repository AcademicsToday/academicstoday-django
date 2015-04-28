from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from registrar.models import Course
from registrar.models import Lecture
from registrar.models import FileUpload
import json
import datetime

# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#
# (2) JSON
# https://docs.djangoproject.com/en/1.7/topics/serialization/


@login_required(login_url='/landpage')
def lecture_notes_page(request, course_id, lecture_id):
    course = Course.objects.get(id=course_id)
    try:
        lecture = Lecture.objects.get(lecture_id=lecture_id)
    except Lecture.DoesNotExist:
        lecture = None
    return render(request, 'course/lecture_note/view.html',{
        'course' : course,
        'lecture' : lecture,
        'NO_VIDEO_PLAYER': settings.NO_VIDEO_PLAYER,
        'YOUTUBE_VIDEO_PLAYER': settings.YOUTUBE_VIDEO_PLAYER,
        'VIMEO_VIDEO_PLAYER': settings.VIMEO_VIDEO_PLAYER,
        'BLIPTV_VIDEO_PLAYER': settings.BLIPTV_VIDEO_PLAYER,
        'user' : request.user,
        'tab' : 'lectures',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def view_lecture_note(request, course_id, lecture_id):
    response_data = {}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                upload_id = int(request.POST['upload_id'])
                note = FileUpload.objects.get(upload_id=upload_id)
            except FileUpload.DoesNotExist:
                note = None
            return render(request, 'course/lecture_note/details.html',{
                'note' : note,
                'NO_VIDEO_PLAYER': settings.NO_VIDEO_PLAYER,
                'YOUTUBE_VIDEO_PLAYER': settings.YOUTUBE_VIDEO_PLAYER,
                'VIMEO_VIDEO_PLAYER': settings.VIMEO_VIDEO_PLAYER,
                'BLIPTV_VIDEO_PLAYER': settings.BLIPTV_VIDEO_PLAYER,
                'user' : request.user,
                'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
                'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
                'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
            })
