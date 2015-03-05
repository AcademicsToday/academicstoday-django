from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from registrar.models import Course
from course.models import Assignment
from course.models import AssignmentSubmission
from course.models import EssayQuestion
from course.models import EssaySubmission
from course.models import MultipleChoiceQuestion
from course.models import MultipleChoiceSubmission
from course.models import ResponseQuestion
from course.models import ResponseSubmission
from course.models import TrueFalseQuestion
from course.models import TrueFalseSubmission
import json
import datetime

# Forms
from course.forms import EssaySubmissionForm
from course.forms import AssignmentSubmissionForm


# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#
# (2) JSON
# https://docs.djangoproject.com/en/1.7/topics/serialization/


@login_required(login_url='/landpage')
def assignments_page(request, course_id):
    course = Course.objects.get(id=course_id)
    
    # Fetch all the assignments for this course.
    try:
        assignments = Assignment.objects.filter(course_id=course_id).order_by('order_num')
    except Assignment.DoesNotExist:
        assignment = None
    
    # Fetch all submitted assignments
    try:
         submitted_assignments = AssignmentSubmission.objects.filter(course_id=course_id,
                                                                     student_id=request.user.id)
    except AssignmentSubmission.DoesNotExist:
        submitted_assignments = None

    # If the submissions & assignment counts do not equal, then we have to
    # iterate through all the assignments and create the missing 'submission'
    # entries for our system.
    if len(assignments) != len(submitted_assignments):
        for assignment in assignments:
            found_assignment = False
            for submitted_assignment in submitted_assignments:
                if assignment.id == submitted_assignment.assignment_id:
                    found_assignment = True
            if not found_assignment:
                submission = AssignmentSubmission.create(
                    student_id=request.user.id,
                    course_id=course_id,
                    assignment_id=assignment.id,
                    type=assignment.type,
                    order_num=assignment.order_num
                )
                submission.save()

    return render(request, 'assignment/list.html',{
        'course' : course,
        'user' : request.user,
        'assignments' : assignments,
        'submitted_assignments' : submitted_assignments,
        'ESSAY_ASSIGNMENT_TYPE' : settings.ESSAY_ASSIGNMENT_TYPE,
        'MULTIPLECHOICE_ASSIGNMENT_TYPE' : settings.MULTIPLECHOICE_ASSIGNMENT_TYPE,
        'TRUEFALSE_ASSIGNMENT_TYPE' : settings.TRUEFALSE_ASSIGNMENT_TYPE,
        'RESPONSE_ASSIGNMENT_TYPE' : settings.RESPONSE_ASSIGNMENT_TYPE,
        'tab' : 'assignments',
        'subtab' : '',
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
    })


@login_required()
def assignment_delete(request, course_id):
    if request.is_ajax():
        if request.method == 'POST':
            student_id = int(request.POST['student_id'])
            assignment_id = int(request.POST['assignment_id'])
            assignment_type = int(request.POST['assignment_type'])
            
            # Update the 'submission_date' of our entry to indicate we
            # have finished the assignment.
            submission = AssignmentSubmission.objects.get(
                assignment_id=int(request.POST['assignment_id']),
                student_id=int(request.POST['student_id']),
                course_id=int(request.POST['course_id'])
            )
            submission.submission_date = None
            submission.save()
            
            # Delete assignments depending on what type
            if assignment_type == settings.ESSAY_ASSIGNMENT_TYPE:
                try:
                    EssaySubmission.objects.get(
                        assignment_id=assignment_id,
                        student_id=student_id,
                        course_id=course_id
                    ).delete()
                    
                    # Send JSON Response indicating success
                    response_data = {'status' : 'success', 'message' : 'assignment was deleted'}
                except EssaySubmission.DoesNotExist:
                    response_data = {'status' : 'failed', 'message' : 'assignment not found'}
            elif assignment_type == settings.MULTIPLECHOICE_ASSIGNMENT_TYPE:
                try:
                    MultipleChoiceSubmission.objects.filter(
                        assignment_id=assignment_id,
                        student_id=student_id,
                        course_id=course_id,
                        exam_id=0,
                    ).delete()
                    response_data = {'status' : 'success', 'message' : 'assignment was deleted'}
                except MultipleChoiceSubmission.DoesNotExist:
                    response_data = {'status' : 'failed', 'message' : 'assignment not found'}
            elif assignment_type == settings.TRUEFALSE_ASSIGNMENT_TYPE:
                try:
                    TrueFalseSubmission.objects.filter(
                        assignment_id=assignment_id,
                        student_id=student_id,
                        course_id=course_id,
                        quiz_id=0,
                    ).delete()
                    response_data = {'status' : 'success', 'message' : 'assignment was deleted'}
                except TrueFalseSubmission.DoesNotExist:
                    response_data = {'status' : 'failed', 'message' : 'assignment not found'}
            elif assignment_type == settings.RESPONSE_ASSIGNMENT_TYPE:
                try:
                    ResponseSubmission.objects.filter(
                        assignment_id=assignment_id,
                        student_id=student_id,
                        course_id=course_id,
                    ).delete()
                    response_data = {'status' : 'success', 'message' : 'assignment was deleted'}
                except ResponseSubmission.DoesNotExist:
                    response_data = {'status' : 'failed', 'message' : 'assignment not found'}
            else:
                response_data = {'status' : 'success', 'message' : ''}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    response_data = {'status' : 'failed', 'message' : 'unknown error with deletion'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def assignment_essay(request, assignment_id):
    response_data = {}
    if request.is_ajax():
        if request.method == 'POST':
            assignment = Assignment.objects.get(id=assignment_id)
            try:
                essay_question = EssayQuestion.objects.get(assignment_id=assignment_id)
            except EssayQuestion.DoesNotExist:
                essay_question = None

            try:
                essay_submission = EssaySubmission.objects.get(assignment_id=assignment_id)
            except EssaySubmission.DoesNotExist:
                essay_submission = None

            return render(request, 'assignment/essay_modal.html',{
                'assignment' : assignment,
                'essay_question' : essay_question,
                'essay_submission' : essay_submission
             })


@login_required()
def upload_essay_assignment(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'error submitting'}
    if request.is_ajax():
        if request.method == 'POST':
            form = EssaySubmissionForm(request.POST, request.FILES)
           
            if form.is_valid():
                form.save()  # Save the form contents to the model
              
                # Update the 'submission_date' of our entry to indicate we
                # have finished the assignment.
                submission = AssignmentSubmission.objects.get(
                    assignment_id=int(request.POST['assignment_id']),
                    student_id=int(request.POST['student_id']),
                    course_id=int(request.POST['course_id'])
                )
                submission.submission_date = datetime.datetime.utcnow()
                submission.save()
              
                response_data = {'status' : 'success', 'message' : 'submitted'}
            else:
                response_data = {'status' : 'failed', 'message' : form.errors}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def assignment_multiplechoice(request, course_id):
    if request.is_ajax():
        if request.method == 'POST':
            assignment_id = int(request.POST['assignment_id'])
            assignment = Assignment.objects.get(id=assignment_id)
            try:
                questions = MultipleChoiceQuestion.objects.filter(
                    assignment_id=assignment_id,
                    course_id=course_id,
                    exam_id=0,
                )
            except MultipleChoiceQuestion.DoesNotExist:
                questions = None
        
            return render(request, 'assignment/mc_modal.html',{
                'assignment' : assignment,
                'questions' : questions,
            })


@login_required()
def submit_mc_assignment_completion(request, course_id):
    # Update the 'submission_date' of our entry to indicate we
    # have finished the assignment.
    submission = AssignmentSubmission.objects.get(
        assignment_id=int(request.POST['assignment_id']),
        student_id=int(request.POST['student_id']),
        course_id=int(request.POST['course_id']),
        exam_id=0,
    )
    submission.submission_date = datetime.datetime.utcnow()
    submission.save()
    
    response_data = {'status' : 'success', 'message' : ''}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def submit_mc_assignment_answer(request, course_id):
    if request.is_ajax():
        if request.method == 'POST':
            assignment_id = int(request.POST['assignment_id'])
            student_id = int(request.POST['student_id'])
            course_id = int(request.POST['course_id'])
            question_num = int(request.POST['num'])
            key = request.POST['key']
            value = request.POST['value']
            # Fetch question and error if not found.
            try:
                question = MultipleChoiceQuestion.objects.get(
                    assignment_id=assignment_id,
                    course_id=course_id,
                    question_num=question_num,
                    exam_id=0,
                )
            except MultipleChoiceQuestion.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'cannot find question'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            
            # Fetch submission and create new submission if not found.
            try:
                submission = MultipleChoiceSubmission.objects.get(
                    student_id=student_id,
                    assignment_id=assignment_id,
                    course_id=course_id,
                    question_num=question_num,
                    exam_id=0,
                )
            except MultipleChoiceSubmission.DoesNotExist:
                submission = MultipleChoiceSubmission.create(
                    student_id=student_id,
                    assignment_id=assignment_id,
                    course_id=course_id,
                    question_num=question_num,
                    exam_id=0,
                )
                submission.save()
                
            # Convert JSON string into Python array
            answers = json.loads(submission.json_answers)
            
            # Append or remove the answers json entry from the submission object.
            found_value = answers.get(key, None)
            if found_value == value:
                answers.pop(key, None)
            else:
                answers[key] = value
            
            # Convert back into JSON string and save
            submission.json_answers = json.dumps(answers)
            submission.save()
            
            response_data = {'status' : 'success', 'message' : ''}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

    response_data = {'status' : 'failed', 'message' : 'error submitting'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def assignment_truefalse(request, course_id):
    if request.is_ajax():
        if request.method == 'POST':
            student_id = int(request.POST['student_id'])
            assignment_id = int(request.POST['assignment_id'])
            assignment = Assignment.objects.get(id=assignment_id)
            
            # Fetch questions
            try:
                questions = TrueFalseQuestion.objects.filter(
                    assignment_id=assignment_id,
                    course_id=course_id,
                    quiz_id=0,
                )
            except TrueFalseQuestion.DoesNotExist:
                questions = None
        
            # Fetch submissions
            try:
                submissions = TrueFalseSubmission.objects.filter(
                    student_id=student_id,
                    assignment_id=assignment_id,
                    course_id=course_id,
                    quiz_id=0,
                )
            except TrueFalseSubmission.DoesNotExist:
                submission = None

            return render(request, 'assignment/truefalse_modal.html',{
                'assignment' : assignment,
                'questions' : questions,
                'submissions' : submissions,
            })


@login_required()
def submit_truefalse_assignment_completion(request, course_id):
    # Update the 'submission_date' of our entry to indicate we
    # have finished the assignment.
    submission = AssignmentSubmission.objects.get(
        assignment_id=int(request.POST['assignment_id']),
        student_id=int(request.POST['student_id']),
        course_id=int(request.POST['course_id'])
    )
    submission.submission_date = datetime.datetime.utcnow()
    submission.save()
                                                  
    response_data = {'status' : 'success', 'message' : ''}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def submit_truefalse_assignment_answer(request, course_id):
    if request.is_ajax():
        if request.method == 'POST':
            assignment_id = int(request.POST['assignment_id'])
            student_id = int(request.POST['student_id'])
            course_id = int(request.POST['course_id'])
            question_num = int(request.POST['num'])
            key = request.POST['key']
            value = request.POST['value']
            
            # Fetch question and error if not found.
            try:
                question = TrueFalseQuestion.objects.get(
                    assignment_id=assignment_id,
                    quiz_id=0,
                    course_id=course_id,
                    question_num=question_num,
                )
            except MultipleChoiceQuestion.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'cannot find question'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        
            # Fetch submission and create new submission if not found.
            try:
                submission = TrueFalseSubmission.objects.get(
                    student_id=student_id,
                    assignment_id=assignment_id,
                    quiz_id=0,
                    course_id=course_id,
                    question_num=question_num,
                )
            except TrueFalseSubmission.DoesNotExist:
                submission = TrueFalseSubmission.create(
                    student_id=student_id,
                    assignment_id=assignment_id,
                    quiz_id=0,
                    course_id=course_id,
                    question_num=question_num,
                )
            
            # Save answer
            submission.answer = key == "true"
            submission.save()

            response_data = {'status' : 'success', 'message' : 'submitted'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

    response_data = {'status' : 'failed', 'message' : 'error submitting'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def assignment_response(request, course_id):
    if request.is_ajax():
        if request.method == 'POST':
            assignment_id = int(request.POST['assignment_id'])
            assignment = Assignment.objects.get(id=assignment_id)
            try:
                questions = ResponseQuestion.objects.filter(
                    assignment_id=assignment_id,
                    course_id=course_id
                )
            except ResponseQuestion.DoesNotExist:
                questions = None
        
            return render(request, 'assignment/response_modal.html',{
                'assignment' : assignment,
                'questions' : questions,
            })


@login_required()
def submit_response_assignment_answer(request, course_id):
    if request.is_ajax():
        if request.method == 'POST':
            assignment_id = int(request.POST['assignment_id'])
            student_id = int(request.POST['student_id'])
            course_id = int(request.POST['course_id'])
            question_num = int(request.POST['question_num'])
            response = request.POST[u'response']
            
            # Fetch submission and create new submission if not found.
            try:
                submission = ResponseSubmission.objects.get(
                    student_id=student_id,
                    assignment_id=assignment_id,
                    course_id=course_id,
                    question_num=question_num,
                )
            except ResponseSubmission.DoesNotExist:
                submission = ResponseSubmission.create(
                    student_id=student_id,
                    assignment_id=assignment_id,
                    course_id=course_id,
                    question_num=question_num,
                )
            
            # Save answer
            submission.answer = response
            submission.save()
            
            response_data = {'status' : 'success', 'message' : response}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

    response_data = {'status' : 'failed', 'message' : 'error submitting'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def submit_response_assignment_completion(request, course_id):
    # Update the 'submission_date' of our entry to indicate we
    # have finished the assignment.
    submission = AssignmentSubmission.objects.get(
        assignment_id=int(request.POST['assignment_id']),
        student_id=int(request.POST['student_id']),
        course_id=int(request.POST['course_id'])
    )
    submission.submission_date = datetime.datetime.utcnow()
    submission.save()
                                                  
    response_data = {'status' : 'success', 'message' : ''}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
