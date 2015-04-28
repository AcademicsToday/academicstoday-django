from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import datetime
from registrar.models import PeerReview
from registrar.models import Course
from registrar.models import Student
from registrar.models import Assignment
from registrar.models import AssignmentSubmission
from registrar.models import EssayQuestion
from registrar.models import EssaySubmission
from registrar.models import MultipleChoiceQuestion
from registrar.models import MultipleChoiceSubmission
from registrar.models import ResponseQuestion
from registrar.models import ResponseSubmission
from registrar.models import TrueFalseQuestion
from registrar.models import TrueFalseSubmission
from student.forms import PeerReviewForm


@login_required(login_url='/landpage')
def peer_reviews_page(request, course_id):
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

    return render(request, 'course/peer_review/assignments_view.html',{
        'course' : course,
        'assignments': assignments,
        'submissions': submissions,
        'user' : request.user,
        'tab' : 'peer_reviews',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def assignment_page(request, course_id, submission_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user)
    a_submission = AssignmentSubmission.objects.get(submission_id=submission_id)
    assignment = a_submission.assignment
    
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
    
    return render(request, 'course/peer_review/question_view.html',{
        'student': student,
        'course': course,
        'assignment': assignment,
        'a_submission': a_submission,
        'e_submissions': e_submissions,
        'r_submissions': r_submissions,
        'ESSAY_QUESTION_TYPE': settings.ESSAY_QUESTION_TYPE,
        'MULTIPLECHOICE_QUESTION_TYPE': settings.MULTIPLECHOICE_QUESTION_TYPE,
        'TRUEFALSE_QUESTION_TYPE': settings.TRUEFALSE_QUESTION_TYPE,
        'RESPONSE_QUESTION_TYPE': settings.RESPONSE_QUESTION_TYPE,
        'user': request.user,
        'tab': 'peer_review',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def peer_review_modal(request, course_id, submission_id):
    response_data = {}
    if request.is_ajax():
        if request.method == 'POST':
            form = PeerReviewForm()
            # Check to see if any fields where missing from the form.
            return render(request, 'course/peer_review/review_modal.html',{
                'question_id': request.POST['question_id'],
                'question_type': request.POST['question_type'],
                'submission_id': request.POST['submission_id'],
                'form': form,
                'user': request.user,
            })


@login_required()
def save_peer_review(request, course_id, submission_id):
    if request.is_ajax():
        if request.method == 'POST':
            question_id = int(request.POST['question_id'])
            question_type = int(request.POST['question_type'])
            
            # Fetch from database
            course = Course.objects.get(id=course_id)
            try:
                a_submission = AssignmentSubmission.objects.get(submission_id=submission_id)
            except AssignmentSubmission.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'cannot find submission'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            assignment = a_submission.assignment
            question = None
            q_submission = None
            if question_type == settings.RESPONSE_QUESTION_TYPE:
                question = ResponseQuestion.objects.get(
                    assignment=assignment,
                    question_id=question_id,
                )
                q_submission = ResponseSubmission.objects.get(
                    question=question,
                    student=a_submission.student,
                )
            elif question_type == settings.ESSAY_QUESTION_TYPE:
                question = EssayQuestion.objects.get(
                    assignment=assignment,
                    question_id=question_id
                )
                q_submission = EssaySubmission.objects.get(
                    question=question,
                    student=a_submission.student,
                )
                    
            # Defensive Code
            if question is None:
                response_data = {'status' : 'failed', 'message' : 'cannot find question at id ' + question_id}
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            if q_submission is None:
                response_data = {'status' : 'failed', 'message' : 'cannot find question submission'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            
            form = PeerReviewForm(request.POST, request.FILES);
            if form.is_valid():
                # Save the peer review
                form.instance.user = request.user
                form.save()
            
                # Save the peer review to the submission
                q_submission.reviews.add(form.instance)
                
                # Indicate success
                response_data = {'status' : 'success', 'message' : 'submitted'}
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def delete_peer_review(request, course_id, submission_id):
    response_data = {'status' : 'failed', 'message' : 'unknown deletion error'}
    if request.is_ajax():
        if request.method == 'POST':
            review_id = request.POST['review_id']
            try:
                peer_review = PeerReview.objects.get(review_id=review_id)
                if peer_review.user == request.user:
                    peer_review.delete()
                    response_data = {'status' : 'success', 'message' : 'deleted'}
                else:
                    response_data = {'status' : 'failed', 'message' : 'unauthorized deletion'}
            except PeerReview.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'record does not exist'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def update_assignment_marks(request, course_id, submission_id):
    response_data = {'status' : 'failed', 'message' : 'unknown deletion error'}
    if request.is_ajax():
        if request.method == 'POST':
            course = Course.objects.get(id=course_id)
            a_submission = AssignmentSubmission.objects.get(submission_id=submission_id)
            e_submissions = EssaySubmission.objects.filter(
                question__assignment=a_submission.assignment,
                student=a_submission.student,
            )
            for e_submission in e_submissions:
                process_submission_question(a_submission, e_submission)

            r_submissions = ResponseSubmission.objects.filter(
                question__assignment=a_submission.assignment,
                student=a_submission.student,
            )
            for r_submission in r_submissions:
                process_submission_question(a_submission, r_submission)
            
            process_submission_assignment(a_submission)
            response_data = {'status' : 'success', 'message' : 'updated'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")



def process_submission_question(a_submission, q_submission):
    # Check how many peer reviews have been made and stop if non where made.
    total_reviews = q_submission.reviews.count()
    if total_reviews == 0:
        q_submission.marks = 0
        q_submission.save()
        return
  
    # Iterate through all the peer reviews and make a distributed weighted
    # average calculation.
    marks = 0
    reviewer_weight = 1 / total_reviews
    for peer_review in q_submission.reviews.all():
        weight = peer_review.marks / 5
        reviewer_mark = weight * q_submission.question.marks
        distributed_mark = reviewer_mark * reviewer_weight
        marks += distributed_mark
    q_submission.marks = marks
    q_submission.save()


def process_submission_assignment(submission):
    assignment = submission.assignment
    student = submission.student
    submission.total_marks = 0
    submission.earned_marks = 0
    
    # Essay Submission(s)
    e_submissions = EssaySubmission.objects.filter(
        student=student,
        question__assignment=assignment,
    )
    for e_submission in e_submissions:
        submission.total_marks += e_submission.question.marks
        submission.earned_marks += e_submission.marks

    # Multiple Choice Submission(s)
    mc_submissions = MultipleChoiceSubmission.objects.filter(
        student=student,
        question__assignment=assignment,
    )
    for mc_submission in mc_submissions:
        submission.total_marks += mc_submission.question.marks
        submission.earned_marks += mc_submission.marks

    # True / False Submission(s)
    tf_submissions = TrueFalseSubmission.objects.filter(
        student=student,
        question__assignment=assignment,
    )
    for tf_submission in tf_submissions:
        submission.total_marks += tf_submission.question.marks
        submission.earned_marks += tf_submission.marks

    # Response Submission(s)
    r_submissions = ResponseSubmission.objects.filter(
        student=student,
        question__assignment=assignment,
    )
    for r_submission in r_submissions:
        submission.total_marks += r_submission.question.marks
        submission.earned_marks += r_submission.marks

    # Compute Percent
    submission.percent = round((submission.earned_marks / submission.total_marks) * 100)
    
    # Save calculation
    submission.save()