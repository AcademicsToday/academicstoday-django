from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import datetime
from registrar.models import Course
from registrar.models import Student
from registrar.models import Assignment
from registrar.models import AssignmentSubmission
from registrar.models import EssayQuestion
from registrar.models import EssaySubmission
from registrar.models import PeerReview
from registrar.models import ResponseQuestion
from registrar.models import ResponseSubmission
from student.forms import PeerReviewForm

# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#
# (2) JSON
# https://docs.djangoproject.com/en/1.7/topics/serialization/

@login_required(login_url='/landpage')
def peer_review_page(request, course_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user)
    
    # Fetch all the assignments for this course.
    try:
        assignments = Assignment.objects.filter(course=course).order_by('assignment_num')
    except Assignment.DoesNotExist:
        assignments = None
    
    # Fetch all submitted assignments
    try:
        submissions = AssignmentSubmission.objects.filter(assignment__course=course)
    except AssignmentSubmission.DoesNotExist:
        submissions = None

    return render(request, 'course/peer_review/assignments_list.html',{
        'course' : course,
        'assignments': assignments,
        'submissions': submissions,
        'user' : request.user,
        'tab' : 'peer_reviews',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def assignment_page(request, course_id, assignment_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user)
    assignment = Assignment.objects.get(assignment_id=assignment_id)
    
    # Load all essay type questions for this assignment.
    try:
        e_submissions = EssaySubmission.objects.filter(question__assignment=assignment)
    except EssayQuestion.DoesNotExist:
        e_submissions = None

    # Load all response type questions for this assignment.
    try:
        r_submissions = ResponseSubmission.objects.filter(question__assignment=assignment)
    except ResponseQuestion.DoesNotExist:
        r_submissions = None
    
    return render(request, 'course/peer_review/question_list.html',{
        'student': student,
        'course': course,
        'assignment': assignment,
        'e_submissions': e_submissions,
        'r_submissions': r_submissions,
        'ESSAY_QUESTION_TYPE': settings.ESSAY_QUESTION_TYPE,
        'MULTIPLECHOICE_QUESTION_TYPE': settings.MULTIPLECHOICE_QUESTION_TYPE,
        'TRUEFALSE_QUESTION_TYPE': settings.TRUEFALSE_QUESTION_TYPE,
        'RESPONSE_QUESTION_TYPE': settings.RESPONSE_QUESTION_TYPE,
        'user': request.user,
        'tab': 'peer_review',
        'local_css_urls': settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def peer_review_modal(request, course_id, assignment_id):
    response_data = {}
    if request.is_ajax():
        if request.method == 'POST':
            question_id = request.POST['question_id']
            form = PeerReviewForm()
            
            # Check to see if any fields where missing from the form.
            return render(request, 'course/peer_review/review_modal.html',{
                'question_id': question_id,
                'form': form,
                'user': request.user,
                'local_css_urls': settings.SB_ADMIN_CSS_LIBRARY_URLS,
                'local_js_urls': settings.SB_ADMIN_JS_LIBRARY_URLS,
            })


@login_required()
def save_peer_review(request, course_id, assignment_id):
    if request.is_ajax():
        if request.method == 'POST':
            question_id = request.POST['question_id']
            # Fetch from database
            course = Course.objects.get(id=course_id)
            assignment = Assignment.objects.get(assignment_id=assignment_id)
            student = Student.objects.get(user=request.user)
            question = EssayQuestion.objects.get(
                assignment=assignment,
                question_id=question_id
            )
            submission = EssaySubmission.objects.get(
                student=student,
                question=question,
            )
            form = PeerReviewForm(request.POST, request.FILES);
            if form.is_valid():
                # Save the peer review
                form.instance.user = request.user
                form.save()
            
                # Save the peer review to the submission
                submission.reviews.add(form.instance)
            
                # Indicate success
                response_data = {'status' : 'success', 'message' : 'submitted'}
            else:
                response_data = {'status' : 'failed', 'message' : form.errors}
            
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def delete_peer_review(request, course_id, assignment_id):
    response_data = {'status' : 'failed', 'message' : 'unknown deletion error'}
    if request.is_ajax():
        if request.method == 'POST':
            review_id = request.POST['review_id']
            review = PeerReview.objects.get(review_id=review_id).delete()
            response_data = {'status' : 'success', 'message' : 'deleted '}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


