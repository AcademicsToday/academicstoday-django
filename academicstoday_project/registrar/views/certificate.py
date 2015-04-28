from django.shortcuts import render
from django.core import serializers
import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from landpage.models import CoursePreview
from registrar.models import Student
from registrar.models import Teacher
from registrar.models import Course
from registrar.models import CourseFinalMark
from registrar.models import CourseSetting


from registrar.forms import CourseForm


@login_required(login_url='/landpage')
def certificates_page(request):
    # Create our student account which will build our registration around.
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = Student.objects.create(user=request.user)
    try:
        marks = CourseFinalMark.objects.filter(student=student)
    except CourseFinalMark.DoesNotExist:
        marks = None

    return render(request, 'registrar/certificate/view.html',{
        'student': student,
        'marks': marks,
        'user': request.user,
        'tab': 'certificates',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS
    })


@login_required()
def certificates_table(request):
    # Create our student account which will build our registration around.
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = Student.objects.create(user=request.user)
    try:
        marks = CourseFinalMark.objects.filter(student=student)
    except CourseFinalMark.DoesNotExist:
        marks = None

    return render(request, 'registrar/certificate/table.html',{
        'student': student,
        'marks': marks,
        'user': request.user,
    })


@login_required(login_url='/landpage')
def change_certificate_accessiblity(request):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            credit_id = int(request.POST['credit_id'])
            try:
                mark = CourseFinalMark.objects.get(credit_id=credit_id)
                if mark.is_public:
                    mark.is_public = False
                else:
                    mark.is_public = True
                mark.save()
                response_data = {'status' : 'success', 'message' : 'certificate accessiblity changed'}
            except CourseFinalMark.DoesNotExist:
                response_data = {'status' : 'failure', 'message' : 'certificate does not exist'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def certificate_page(request, credit_id):
    # Create our student account which will build our registration around.
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = Student.objects.create(user=request.user)
    try:
        mark = CourseFinalMark.objects.get(credit_id=credit_id)
    except CourseFinalMark.DoesNotExist:
        mark = None

    return render(request, 'registrar/certificate/certificate.html',{
        'student': student,
        'mark': mark,
        'user': request.user,
        'tab': 'certificates',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS
    })


@login_required()
def certificate_permalink_modal(request):
    credit_id = int(request.POST['credit_id'])
    try:
        mark = CourseFinalMark.objects.get(credit_id=credit_id)
    except CourseFinalMark.DoesNotExist:
        mark = None
    return render(request, 'registrar/certificate/permalink_modal.html',{
        'mark': mark,
        'user': request.user,
        'tab': 'certificates',
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS
    })

