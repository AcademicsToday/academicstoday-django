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
from registrar.models import AssignmentSubmission
from registrar.models import QuizSubmission
from registrar.models import ExamSubmission
from registrar.models import CourseFinalMark


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
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS,
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
            response_data = {'status' : 'success', 'message' : 'changed'}
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
    try:
        a_submissions = AssignmentSubmission.objects.filter(
            assignment__course=course,
            student=student,
        )
    except AssignmentSubmission.DoesNotExist:
        a_submissions = None
    try:
        q_submissions = QuizSubmission.objects.filter(
            quiz__course=course,
            student=student,
        )
    except QuizSubmission.DoesNotExist:
        q_submissions = None
    
    try:
        e_submissions = ExamSubmission.objects.filter(
            exam__course=course,
            student=student,
        )
    except ExamSubmission.DoesNotExist:
        e_submissions = None

    # Calculate the final mark for the course.
    has_completed_final = False
    final_percent = 0
    for a_submission in a_submissions:
        percent = (a_submission.assignment.worth / 100)
        percent *= (a_submission.percent / 100)
        final_percent += percent
    for q_submission in q_submissions:
        percent = (q_submission.quiz.worth / 100)
        percent *= (q_submission.percent / 100)
        final_percent += percent
    for e_submission in e_submissions:
        percent = (e_submission.exam.worth / 100)
        percent *= (e_submission.percent / 100)
        final_percent += percent
        if e_submission.exam.is_final:
            if percent >= 0.50:
                has_completed_final = True
    final_percent *= 100

    # Validation
    if final_percent < 50:
        return
    if not has_completed_final:
        return
        
    # Grant credit or update credit.
    try:
        final_mark = CourseFinalMark.objects.get(
            course=course,
            student=student,
        )
        final_mark.percent = final_percent
        final_mark.save()
    except CourseFinalMark.DoesNotExist:
        final_mark = CourseFinalMark.objects.create(
            course=course,
            student=student,
            percent = final_percent,
        )
        final_mark.save()

