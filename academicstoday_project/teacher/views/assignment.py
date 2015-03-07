from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import datetime
from registrar.models import Teacher
from registrar.models import Student
from registrar.models import Course
from registrar.models import Assignment
from teacher.forms import AssignmentForm

# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#

@login_required(login_url='/landpage')
def assignments_page(request, course_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)

    try:
        assignments = Assignment.objects.filter(course=course).order_by('-assignment_num')
    except Assignment.DoesNotExist:
        assignments = None
    return render(request, 'teacher/assignment/list.html',{
        'teacher' : teacher,
        'course' : course,
        'assignments' : assignments,
        'user' : request.user,
        'tab' : 'assignments',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
    })

@login_required(login_url='/landpage')
def assignment_modal(request, course_id):
    if request.method == u'POST':
        # Get the assignment_id of post and either create a brand new form
        # for the user, or load up existing one based on the database
        # data for the particular assignment.
        assignment_id = int(request.POST['assignment_id'])
        form = None
        if assignment_id > 0:
            assignment = Assignment.objects.get(assignment_id=assignment_id)
            form = AssignmentForm(instance=assignment)
        else:
            form = AssignmentForm()
        return render(request, 'teacher/assignment/modal.html',{
            'form' : form,
        })


@login_required(login_url='/landpage')
def save_assignment(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            course = Course.objects.get(id=course_id)
            assignment_id = int(request.POST['assignment_id'])
            form = None
            
            # If assignment already exists, then lets update only, else insert.
            if assignment_id > 0:
                assignment = Assignment.objects.get(assignment_id=assignment_id)
                form = AssignmentForm(instance=assignment, data=request.POST)
            else:
                form = AssignmentForm(request.POST, request.FILES)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.course = course
                instance.save()
                response_data = {'status' : 'success', 'message' : 'saved'}
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def delete_assignment(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deleting'}
    if request.is_ajax():
        if request.method == 'POST':
            assignment_id = int(request.POST['assignment_id'])
            lassignment = Assignment.objects.get(assignment_id=assignment_id)
            assignment.delete()
            response_data = {'status' : 'success', 'message' : 'deleted'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def assignment_page(request, course_id, assignment_id):
    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(user=request.user)
    
    try:
        assignments = Assignment.objects.filter(course=course).order_by('-assignment_num')
    except Assignment.DoesNotExist:
        assignments = None
    return render(request, 'teacher/assignment/details.html',{
        'teacher' : teacher,
        'course' : course,
        'assignments' : assignments,
        'user' : request.user,
        'tab' : 'assignments',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
    })
