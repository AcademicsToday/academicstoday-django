from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import datetime
from registrar.models import Course
from registrar.models import CourseSubmission
from registrar.models import Student


@login_required(login_url='/landpage')
def settings_page(request, course_id):
    course = Course.objects.get(id=course_id)
    try:
        review = CourseSubmission.objects.get(course=course)
    except CourseSubmission.DoesNotExist:
        review = None
    return render(request, 'teacher/setting/view.html',{
        'course': course,
        'review': review,
        'COURSE_SUBMITTED_FOR_REVIEW_STATUS': settings.COURSE_SUBMITTED_FOR_REVIEW_STATUS,
        'COURSE_IN_REVIEW_STATUS': settings.COURSE_IN_REVIEW_STATUS,
        'COURSE_UNAVAILABLE_STATUS': settings.COURSE_UNAVAILABLE_STATUS,
        'COURSE_AVAILABLE_STATUS': settings.COURSE_AVAILABLE_STATUS,
        'COURSE_REJECTED_STATUS': settings.COURSE_REJECTED_STATUS,
        'user': request.user,
        'tab': 'settings',
        'local_css_urls': settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def suspend_course(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            # Fetch objects
            course = Course.objects.get(id=course_id)
            if course.status == settings.COURSE_UNAVAILABLE_STATUS:
                course.status = settings.COURSE_AVAILABLE_STATUS
            else:
                mark_students(course)
                course.status = settings.COURSE_UNAVAILABLE_STATUS
            course.save();
            response_data = {'status' : 'success', 'message' : ''}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


# Private

def mark_students(course):
    try:
        students = Student.objects.filter(courses__id=course.id)
        for student in students:
            mark_student(course, student)
    except Student.DoesNotExist:
        pass


def mark_student(course, student):
    pass  #TODO: Implement