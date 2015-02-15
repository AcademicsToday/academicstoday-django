from django.shortcuts import render
from django.core import serializers
from .models import LandpageTeamMember
from .models import LandpageCoursePreview
from .models import CoursePreview
from .models import Course
from .models import CourseEnrollment
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


agency_css_library_urls = ["lib/jquery/1.11.1/jquery-ui.css",
                           "lib/bootstrap/3.2.0/css/bootstrap.min.css",
                           "lib/font-awesome/4.1.0/css/font-awesome.css",
                           "lib/font-awesome/4.1.0/css/font-awesome.min.css",
                           "css/landpage.css",
                           "css/agency.css"]

sb_admin_css_library_urls = ["lib/jquery/1.11.1/jquery-ui.css",
                             "lib/bootstrap/3.3.2/css/bootstrap.min.css",
                             "lib/font-awesome/4.2.0/css/font-awesome.css",
                             "lib/font-awesome/4.2.0/css/font-awesome.min.css",
                             "css/sb-admin.css"]

agency_js_library_urls = ["lib/jquery/1.11.1/jquery.min.js",
                          "lib/jquery/1.11.1/jquery.tablesorter.js",
                          "lib/jquery/1.11.1/jquery-ui.js",
                          "lib/jquery-easing/1.3/jquery.easing.min.js",
                          "lib/bootstrap/3.2.0/js/bootstrap.min.js",
                          "lib/bootstrap/3.2.0/js/bootstrap.js",
                          "lib/bootstrap/3.2.0/js/tab.js",
                          "lib/bootstrap/3.2.0/js/popover.js",
                          "lib/bootstrap/3.2.0/js/tooltip.js",
                          "lib/bootstrap/3.2.0/js/button.js",
                          "lib/bootstrap/3.2.0/js/modal.js",
                          "lib/bootstrap/3.2.0/js/functions.js",
                          "lib/bootstrap/3.2.0/js/collapse.js",
                          "lib/bootstrap/3.2.0/js/transition.js",
                          "lib/classie/1.0.0/classie.js",
                          "lib/cbpanimatedheader/1.0.0/cbpAnimatedHeader.js",
                          "lib/cbpanimatedheader/1.0.0/cbpAnimatedHeader.min.js",
                          "lib/jqbootstrapvalidation/1.3.6/jqBootstrapValidation.js"]

sb_admin_js_library_urls = ["lib/jquery/1.11.1/jquery.min.js",
                            "lib/jquery/1.11.1/jquery.tablesorter.js",
                            "lib/jquery/1.11.1/jquery-ui.js",
                            "lib/jquery-easing/1.3/jquery.easing.min.js",
                            "lib/bootstrap/3.3.2/js/bootstrap.min.js",
                            "lib/bootstrap/3.3.2/js/bootstrap.js",
#                            "lib/morris/0.5.0/morris.js",
#                            "lib/morris/0.5.0/morris.min.js",
                            "lib/morris/0.5.0/raphael.min.js",
#                            "lib/morris/0.5.0/morris-data.js",
#                            "lib/flot/x.x/excanvas.min.js",
#                            "lib/flot/x.x/flot-data.js",
#                            "lib/flot/x.x/jquery.flot.js",
#                            "lib/flot/x.x/jquery.flot.pie.js",
#                            "lib/flot/x.x/jquery.flot.resize.js",
#                            "lib/flot/x.x/jquery.flot.tooltip.min.js",
                            ]


def load_landpage(request):
    course_previews = LandpageCoursePreview.objects.all();
    team_members = LandpageTeamMember.objects.all()
    return render(request, 'landpage/main.html',{
    'course_previews' : course_previews,
    'team_members' : team_members,
    'local_css_urls' : agency_css_library_urls,
    'local_js_urls' : agency_js_library_urls})


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


def register(request):
    response_data = {}
    if request.is_ajax():
        if request.method == 'POST':
            # Check to see if any fields where missing from the form.
            if request.POST['first_name'] == '':
                response_data = {'status' : 'failure', 'message' : 'Missing first name.' }
            elif request.POST['last_name'] == '':
                response_data = {'status' : 'failure', 'message' : 'Missing last name.' }
            elif request.POST.get('email') == '':
                response_data = {'status' : 'failure', 'message' : 'Missing email.' }
            elif request.POST['password'] == '':
                response_data = {'status' : 'failure', 'message' : 'Missing password.' }
            elif request.POST['password_repeated'] == '':
                response_data = {'status' : 'failure', 'message' : 'Missing password repeated again.' }
            elif request.POST['is_18_or_plus'] == 'false':
                response_data = {'status' : 'failure', 'message' : 'You must be 18 or over.' }
            elif request.POST['password'] != request.POST['password_repeated']:
                response_data = {'status' : 'failure', 'message' : 'Passwords do not match.' }
            else:
                # Check to see if we already have the username or email taken.
                try:
                    user = User.objects.get(email__exact=request.POST['email'])
                    response_data = {'status' : 'failure', 'message' : 'Email already exists, please choose another email' }
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
                except User.DoesNotExist:
                    pass

                # Create the user in our database
                try:
                    user = User.objects.create_user(request.POST['email'], request.POST['email'], request.POST['password'])
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.save()
                    response_data = {'status' : 'success', 'message' : 'You are now successfully registered' }
                except Exception as e:
                    response_data = {'status' : 'failure', 'message' : 'An unknown error occured, failed registering.' }
        else:
            response_data = {'status' : 'failure', 'message' : 'Not acceptable request made.' }

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def login_authentication(request):
    response_data = {}
    if request.is_ajax():
        if request.method == 'POST':
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            
            # Does the user exist for the username and has correct password?
            if user is not None:
                # Is user suspended or active?
                if user.is_active:
                    response_data = {'status' : 'success', 'message' : 'Loging in...'}
                    login(request, user)
                else:
                    response_data = {'status' : 'failure', 'message' : 'You are suspended.'}
            else:
                response_data = {'status' : 'failure', 'message' : 'Wrong username or password.'}                
    return HttpResponse(json.dumps(response_data), content_type="application/json")


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


@login_required(login_url='/landpage')
def course(request, course_id, tab):
    course = Course.objects.get(id=course_id)
    return render(request, 'course/home.html',{
                  'course' : course,
                  'user' : request.user,
                  'tab' : tab,
                  'local_css_urls' : sb_admin_css_library_urls,
                  'local_js_urls' : sb_admin_js_library_urls})


@login_required(login_url='/landpage')
def course_home(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'course/home.html',{
                  'course' : course,
                  'user' : request.user,
                  'tab' : 'home',
                  'local_css_urls' : sb_admin_css_library_urls,
                  'local_js_urls' : sb_admin_js_library_urls})

@login_required(login_url='/landpage')
def course_syllabus(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'course/syllabus.html',{
                  'course' : course,
                  'user' : request.user,
                  'tab' : 'syllabus',
                  'local_css_urls' : sb_admin_css_library_urls,
                  'local_js_urls' : sb_admin_js_library_urls})

@login_required(login_url='/landpage')
def course_policy(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'course/policy.html',{
                  'course' : course,
                  'user' : request.user,
                  'tab' : 'policy',
                  'local_css_urls' : sb_admin_css_library_urls,
                  'local_js_urls' : sb_admin_js_library_urls})

@login_required(login_url='/landpage')
def course_lectures(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'course/lectures.html',{
                  'course' : course,
                  'user' : request.user,
                  'tab' : 'lectures',
                  'local_css_urls' : sb_admin_css_library_urls,
                  'local_js_urls' : sb_admin_js_library_urls})

@login_required(login_url='/landpage')
def course_assignments(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'course/assignments.html',{
                  'course' : course,
                  'user' : request.user,
                  'tab' : 'assignments',
                  'local_css_urls' : sb_admin_css_library_urls,
                  'local_js_urls' : sb_admin_js_library_urls})

@login_required(login_url='/landpage')
def course_quizzes(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'course/quizzes.html',{
                  'course' : course,
                  'user' : request.user,
                  'tab' : 'quizzes',
                  'local_css_urls' : sb_admin_css_library_urls,
                  'local_js_urls' : sb_admin_js_library_urls})

@login_required(login_url='/landpage')
def course_exams(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'course/exams.html',{
                  'course' : course,
                  'user' : request.user,
                  'tab' : 'exams',
                  'local_css_urls' : sb_admin_css_library_urls,
                  'local_js_urls' : sb_admin_js_library_urls})

@login_required(login_url='/landpage')
def course_discussion(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'course/discussion.html',{
                  'course' : course,
                  'user' : request.user,
                  'tab' : 'discussion',
                  'local_css_urls' : sb_admin_css_library_urls,
                  'local_js_urls' : sb_admin_js_library_urls})