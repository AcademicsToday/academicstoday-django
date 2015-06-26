from django.shortcuts import render
from django.core import serializers

from landpage.models import LandpageTeamMember
from landpage.models import LandpageTopPickCourse
from landpage.models import LandpageCoursePreview
from landpage.models import CoursePreview
from landpage.models import LandpageContactMessage
from landpage.models import LandpagePartner
from registrar.models import Course
from landpage.form import ContactForm

import json
from django.http import HttpResponse
from django.conf import settings


def landpage_page(request):
    top_courses = LandpageTopPickCourse.objects.all()
    course_previews = LandpageCoursePreview.objects.all()
    team_members = LandpageTeamMember.objects.all().order_by('id')
    partners = LandpagePartner.objects.all()
    contact_form = ContactForm()
    return render(request, 'landpage/main/index.html',{
        'top_courses': top_courses,
        'course_previews' : course_previews,
        'team_members' : team_members,
        'partners': partners,
        'contact_form': contact_form,
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls' : settings.AGENCY_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.AGENCY_JS_LIBRARY_URLS
    })


def course_preview_modal(request):
    course = None
    if request.method == u'POST':
        POST = request.POST
        course_id = POST.get('course_id')
        if course_id is not None:
            try:
                course = Course.objects.get(id=int(course_id))
            except Course.DoesNotExist:
                pass
    return render(request, 'landpage/main/course_preview.html',{
        'course' : course
    })


def save_contact_us_message(request):
    response_data = {'status' : 'failed', 'message' : 'unknown error with sending message'}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                form = ContactForm(request.POST)
            
                # Validate the form: the captcha field will automatically
                # check the input
                if form.is_valid():
                    name = request.POST['name']
                    email = request.POST['email']
                    phone = request.POST['phone']
                    message = request.POST['message']
                
                    # Save our message.
                    LandpageContactMessage.objects.create(
                        name=name,
                        email=email,
                        phone=phone,
                        message=message,
                    ).save()
                    response_data = {'status' : 'success', 'message' : 'saved'}
                else:
                    response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
            except:
                response_data = {
                    'status' : 'failure',
                    'message' : 'could not save message ' + name + ' ' + email + ' ' + phone + ' ' + message
                }
    return HttpResponse(json.dumps(response_data), content_type="application/json")
