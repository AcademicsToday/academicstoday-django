from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import datetime
import os
from registrar.models import Teacher
from registrar.models import Student
from registrar.models import Course
from registrar.models import Lecture
from registrar.models import FileUpload
from teacher.forms import LectureForm
from teacher.forms import NoteUploadForm


@login_required(login_url='/landpage')
def lecture_notes_page(request, course_id, lecture_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)
    lecture = Lecture.objects.get(lecture_id=lecture_id)
    return render(request, 'teacher/lecture_note/view.html',{
        'teacher' : teacher,
        'course' : course,
        'lecture' : lecture,
        'user' : request.user,
        'tab' : 'lecture_notes',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def lecture_notes_table(request, course_id, lecture_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)
    lecture = Lecture.objects.get(lecture_id=lecture_id)
    return render(request, 'teacher/lecture_note/table.html',{
        'teacher' : teacher,
        'course' : course,
        'lecture' : lecture,
        'user' : request.user,
    })


@login_required(login_url='/landpage')
def lecture_note_modal(request, course_id, lecture_id):
    if request.method == u'POST':
        # Get the lecture_id of post and either create a brand new form
        # for the user, or load up existing one based on the database
        # data for the particular lecture.
        form = None
        lecture_id = int(lecture_id)
        upload_id = int(request.POST['upload_id'])
        if upload_id > 0:
            upload = FileUpload.objects.get(upload_id=upload_id)
            form = NoteUploadForm(instance=upload)
        else:
            form = NoteUploadForm()
        
        course = Course.objects.get(id=course_id)
        lecture = Lecture.objects.get(lecture_id=lecture_id)
        return render(request, 'teacher/lecture_note/modal.html',{
            'course': course,
            'lecture': lecture,
            'form': form,
        })


@login_required(login_url='/landpage')
def save_lecture_note(request, course_id, lecture_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            course = Course.objects.get(id=course_id)
            lecture_id = int(lecture_id)
            lecture = Lecture.objects.get(lecture_id=lecture_id)
            form = NoteUploadForm(request.POST, request.FILES)
            form.instance.type = settings.PDF_FILE_UPLOAD_TYPE
            form.instance.user = request.user
            upload_id = int(request.POST['upload_id'])
            
            # If lecture already exists, then delete local file.
            if upload_id > 0:
                # Delete previous file.
                try:
                    upload = FileUpload.objects.get(upload_id=upload_id)
                except FileUpload.DoesNotExist:
                    return HttpResponse(json.dumps({
                        'status' : 'failed', 'message' : 'record does not exist'
                    }), content_type="application/json")

                if upload.file:
                    if os.path.isfile(upload.file.path):
                        os.remove(upload.file.path)
                        upload.file = None
                        upload.save()
                form.instance = upload
                
            # Save if valid
            if form.is_valid():
                form.save()
                
                # Keep track of notes in lecture.
                if upload_id == 0:
                    lecture.notes.add(form.instance)
                
                response_data = {'status' : 'success', 'message' : 'saved'}
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def delete_lecture_note(request, course_id, lecture_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deleting'}
    if request.is_ajax():
        if request.method == 'POST':
            upload_id = int(request.POST['upload_id'])
            try:
                upload = FileUpload.objects.get(upload_id=upload_id)
                if upload.user == request.user:
                    upload.delete()
                    response_data = {'status' : 'success', 'message' : 'deleted'}
                else:
                    response_data = {'status' : 'failed', 'message' : 'unauthorized deletion'}
            except FileUpload.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'record not found'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
