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
from registrar.models import AssignmentSubmission
from registrar.models import QuizSubmission
from registrar.models import ExamSubmission

@login_required(login_url='/landpage')
def credit_page(request, course_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user)
    try:
        final_mark = CourseFinalMark.objects.get(
            course=course,
            student=student,
        )
    except CourseFinalMark.DoesNotExist:
        final_mark = None
    
    return render(request, 'course/credit/list.html',{
        'course' : course,
        'final_mark': final_mark,
        'user' : request.user,
        'tab' : 'credit',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
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
                response_data = {'status' : 'failure', 'message' : 'you need to pass with at minimum 50%'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            if not has_completed_final:
                response_data = {'status' : 'failure', 'message' : 'you need to pass the final exam with at minumum 50%'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")

            # Create or fetch our final mark for this course
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
            response_data = {'status' : 'success', 'message' : 'credit granted'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def error_credits_modal(request, course_id, submission_id):
    response_data = {}
    if request.is_ajax():
        if request.method == 'POST':
        
            # Check to see if any fields where missing from the form.
            return render(request, 'course/peer_review/review_modal.html',{
                'user': request.user,
            })