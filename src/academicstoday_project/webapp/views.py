from django.shortcuts import render
from django.core import serializers
from .models import LandpageTeamMember
from .models import LandpageCoursePreview
from .models import CoursePreview

# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#
# (2) JSON
# https://docs.djangoproject.com/en/1.7/topics/serialization/

# Create your views here...

def load_landpage(request):
    local_css_library_urls = ["lib/jquery/1.11.1/jquery-ui.css",
                              "lib/bootstrap/3.2.0/css/bootstrap.min.css",
                              "lib/font-awesome/4.1.0/css/font-awesome.css",
                              "lib/font-awesome/4.1.0/css/font-awesome.min.css",
                              "css/landpage.css"]
    local_js_library_urls = ["lib/jquery/1.11.1/jquery.min.js",
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
    course_previews = LandpageCoursePreview.objects.all();
    team_members = LandpageTeamMember.objects.all()
    return render(request, 'landpage/main.html',{
    'course_previews' : course_previews,
    'team_members' : team_members,
    'local_css_urls' : local_css_library_urls,
    'local_js_urls' : local_js_library_urls})

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
