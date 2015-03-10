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
from registrar.models import Announcement
from registrar.models import Syllabus
from registrar.models import Policy
from registrar.models import Lecture
from registrar.models import Assignment
from registrar.models import Quiz
from registrar.models import Exam

@login_required(login_url='/landpage')
def overview_page(request, course_id):
    course = Course.objects.get(id=course_id)

    try:
        announcements = Announcement.objects.filter(course=course).order_by('-post_date')
    except Announcement.DoesNotExist:
        announcements = None

    try:
        syllabus = Syllabus.objects.get(course=course)
    except Syllabus.DoesNotExist:
        syllabus = None

    try:
        policy = Policy.objects.get(course=course)
    except Policy.DoesNotExist:
        policy = None

    try:
        lectures = Lecture.objects.filter(course=course).order_by('-lecture_num')
    except Lecture.DoesNotExist:
        lectures = None

    try:
        assignments = Assignment.objects.filter(course=course).order_by('-assignment_num')
    except Assignment.DoesNotExist:
        assignments = None

    try:
        quizzes = Quiz.objects.filter(course=course).order_by('-quiz_num')
    except Quiz.DoesNotExist:
        quizzes = None

    try:
        exams = Exam.objects.filter(course=course).order_by('-exam_num')
    except Exam.DoesNotExist:
        exams = None

    return render(request, 'teacher/overview/view.html',{
        'course' : course,
        'announcements' : announcements,
        'syllabus': syllabus,
        'lectures': lectures,
        'assignments': assignments,
        'quizzes': quizzes,
        'exams': exams,
        'policy': policy,
        'user' : request.user,
        'tab' : 'overview',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
    })
