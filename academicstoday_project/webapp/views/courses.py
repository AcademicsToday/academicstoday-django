from django.shortcuts import render
from django.core import serializers
from webapp.models import CoursePreview
from webapp.models import Course
from webapp.models import CourseEnrollment
import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#
# (2) JSON
# https://docs.djangoproject.com/en/1.7/topics/serialization/

sb_admin_css_library_urls = ["js/jquery/1.11.1/jquery-ui.css",
                             "js/bootstrap/3.3.2/css/bootstrap.min.css",
                             "js/font-awesome/4.2.0/css/font-awesome.css",
                             "js/font-awesome/4.2.0/css/font-awesome.min.css",
                             "css/sb-admin.css"]

sb_admin_js_library_urls = ["js/jquery/1.11.1/jquery.min.js",
                            "js/jquery/1.11.1/jquery.tablesorter.js",
                            "js/jquery/1.11.1/jquery-ui.js",
                            "js/jquery-easing/1.3/jquery.easing.min.js",
                            "js/bootstrap/3.3.2/js/bootstrap.min.js",
                            "js/bootstrap/3.3.2/js/bootstrap.js",
#                            "js/morris/0.5.0/morris.js",
#                            "js/morris/0.5.0/morris.min.js",
                            "js/morris/0.5.0/raphael.min.js",
#                            "js/morris/0.5.0/morris-data.js",
#                            "js/flot/x.x/excanvas.min.js",
#                            "js/flot/x.x/flot-data.js",
#                            "js/flot/x.x/jquery.flot.js",
#                            "js/flot/x.x/jquery.flot.pie.js",
#                            "js/flot/x.x/jquery.flot.resize.js",
#                            "js/flot/x.x/jquery.flot.tooltip.min.js",
                            ]

def logout_authentication(request):
    response_data = {'status' : 'success', 'message' : 'Done'}
    if request.is_ajax():
        if request.method == 'POST':
            logout(request)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def courses(request):
    courses = Course.objects.all()
    return render(request, 'courses/list.html',{
                  'courses' : courses,
                  'user' : request.user,
                  'local_css_urls' : sb_admin_css_library_urls,
                  'local_js_urls' : sb_admin_js_library_urls})


@login_required()
def enroll(request):
    response_data = {'status' : 'failure', 'message' : 'unsupported request format'}
    if request.is_ajax():
        user_id = request.user.id
        course_id = request.POST['course_id']
        
        if course_id == '':
            response_data = {'status' : 'failure', 'message' : 'Missing course_id.' }
        else:
            # Check to see if the user is enrolled, if not, enroll user.
            try:
                enrollment = CourseEnrollment.objects.get(id=user_id,course_id=course_id)
            except CourseEnrollment.DoesNotExist:
                # Create new record.
                enrollment = CourseEnrollment.create(course_id=course_id, user_id=user_id)
                enrollment.save()
                    
            # Indicate the user is enrolled
            response_data = {'status' : 'success', 'message' : 'enrolled' }
    return HttpResponse(json.dumps(response_data), content_type="application/json")