from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import datetime
from registrar.models import Course
from registrar.models import CourseFinalMark
from registrar.models import Student


@login_required(login_url='/landpage')
def credit_page(request, course_id):
    course = Course.objects.get(id=course_id)
    
    return render(request, 'course/credit/list.html',{
        'course' : course,
        'user' : request.user,
        'tab' : 'credit',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
    })


# Function will verify that all criteria to pass the course are met and
# make a record of user completing this course. If user does not meet
# criteria an error will be returned.
@login_required()
def submit_credit_application(request, course_id):
    if request.is_ajax():
        if request.method == 'POST':
            # Fetch from database
            course = Course.objects.get(id=course_id)
            student = Student.objects.get(user=request.user)
            
            #TODO: Validate
            
            #TODO: Final Mark submission
            
            response_data = {'status' : 'success', 'message' : 'submitted'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def error_credits_modal(request, course_id, submission_id):
    response_data = {}
    if request.is_ajax():
        if request.method == 'POST':
        
            # Check to see if any fields where missing from the form.
            return render(request, 'course/peer_review/review_modal.html',{
                'user': request.user,
                'local_css_urls': settings.SB_ADMIN_CSS_LIBRARY_URLS,
                'local_js_urls': settings.SB_ADMIN_JS_LIBRARY_URLS,
            })