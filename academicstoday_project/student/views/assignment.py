from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
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
import json
import datetime

# Forms
from student.forms import EssaySubmissionForm
from student.forms import AssignmentSubmissionForm


@login_required(login_url='/landpage')
def assignments_page(request, course_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user)

    # Fetch all the assignments for this course.
    try:
        assignments = Assignment.objects.filter(course=course).order_by('assignment_num')
    except Assignment.DoesNotExist:
        assignment = None

    # Fetch all submitted assignments
    try:
        submitted_assignments = AssignmentSubmission.objects.filter(assignment__course=course,
                                                                    student=student)
    except AssignmentSubmission.DoesNotExist:
        submitted_assignments = None

    # If the submissions & assignment counts do not equal, then we have to
    # iterate through all the assignments and create the missing 'submission'
    # entries for our system.
    if len(assignments) != len(submitted_assignments):
        for assignment in assignments:
            found_assignment = False
            for submitted_assignment in submitted_assignments:
                if assignment.assignment_id == submitted_assignment.assignment_id:
                    found_assignment = True
            if not found_assignment:
                submission = AssignmentSubmission.objects.create(
                    student=student,
                    assignment=assignment,
                )
                submission.save()
        # Once we saved the data, we will have to fetch the results again.
        submitted_assignments = AssignmentSubmission.objects.filter(
            assignment__course=course,
            student=student
        )

    return render(request, 'course/assignment/assignments_list.html',{
        'course' : course,
        'user' : request.user,
        'submitted_assignments' : submitted_assignments,
        'ESSAY_QUESTION_TYPE' : settings.ESSAY_QUESTION_TYPE,
        'MULTIPLECHOICE_QUESTION_TYPE' : settings.MULTIPLECHOICE_QUESTION_TYPE,
        'TRUEFALSE_QUESTION_TYPE' : settings.TRUEFALSE_QUESTION_TYPE,
        'RESPONSE_QUESTION_TYPE' : settings.RESPONSE_QUESTION_TYPE,
        'tab' : 'assignments',
        'subtab' : '',
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
        e_questions = EssayQuestion.objects.filter(assignment=assignment).order_by('question_num')
    except EssayQuestion.DoesNotExist:
        e_questions = None
    try:
        e_submissions = EssaySubmission.objects.filter(question__assignment=assignment, student=student)
    except EssayQuestion.DoesNotExist:
        e_submissions = None

    # Load all multiple-choice type questions/submissions for this assignment.
    try:
        mc_questions = MultipleChoiceQuestion.objects.filter(assignment=assignment).order_by('question_num')
    except MultipleChoiceQuestion.DoesNotExist:
        mc_questions = None
    try:
        mc_submissions = MultipleChoiceSubmission.objects.filter(question__assignment=assignment, student=student)
    except MultipleChoiceSubmission.DoesNotExist:
        mc_submissions = None

    # Load all true/false type questions/submissions for this assignment.
    try:
        tf_questions = TrueFalseQuestion.objects.filter(assignment=assignment).order_by('question_num')
    except TrueFalseQuestion.DoesNotExist:
        tf_questions = None
    try:
        tf_submissions = TrueFalseSubmission.objects.filter(question__assignment=assignment, student=student)
    except tf_submissions.DoesNotExist:
        tf_submissions = None

    # Load all response type questions for this assignment.
    try:
        r_questions = ResponseQuestion.objects.filter(assignment=assignment).order_by('question_num')
    except ResponseQuestion.DoesNotExist:
        r_questions = None
    try:
        r_submissions = ResponseSubmission.objects.filter(question__assignment=assignment, student=student)
    except ResponseQuestion.DoesNotExist:
        r_submissions = None

    return render(request, 'course/assignment/question_list.html',{
        'student': student,
        'course': course,
        'assignment': assignment,
        'e_questions': e_questions,
        'e_submissions': e_submissions,
        'mc_questions': mc_questions,
        'mc_submissions': mc_submissions,
        'tf_questions': tf_questions,
        'tf_submissions': tf_submissions,
        'r_questions': r_questions,
        'r_submissions': r_submissions,
        'ESSAY_QUESTION_TYPE': settings.ESSAY_QUESTION_TYPE,
        'MULTIPLECHOICE_QUESTION_TYPE': settings.MULTIPLECHOICE_QUESTION_TYPE,
        'TRUEFALSE_QUESTION_TYPE': settings.TRUEFALSE_QUESTION_TYPE,
        'RESPONSE_QUESTION_TYPE': settings.RESPONSE_QUESTION_TYPE,
        'user': request.user,
        'tab': 'assignment',
        'local_css_urls': settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_JS_LIBRARY_URLS,
    })



@login_required()
def delete_assignment(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deletion'}
    if request.is_ajax():
        if request.method == 'POST':
            assignment_id = int(request.POST['assignment_id'])
            course = Course.objects.get(id=course_id)
            student = Student.objects.get(user=request.user)
            assignment = Assignment.objects.get(assignment_id=assignment_id)

            # Set 'is_finished' to false to indicate we need to take the
            # assignment all over.
            submission = AssignmentSubmission.objects.get(
                student=student,
                assignment=assignment,
            )
            submission.is_finished = False
            submission.save()
            
            # Delete all previous entries.
            try:
                e_submissions = EssaySubmission.objects.filter(question__assignment=assignment, student=student)
                e_submissions.delete()
            except EssayQuestion.DoesNotExist:
                pass
            try:
                mc_submissions = MultipleChoiceSubmission.objects.filter(question__assignment=assignment, student=student)
                mc_submissions.delete()
            except MultipleChoiceSubmission.DoesNotExist:
                pass
            try:
                tf_submissions = TrueFalseSubmission.objects.filter(question__assignment=assignment, student=student)
                tf_submissions.delete()
            except tf_submissions.DoesNotExist:
                pass
            try:
                r_submissions = ResponseSubmission.objects.filter(question__assignment=assignment, student=student)
                r_submissions.delete()
            except ResponseQuestion.DoesNotExist:
                pass

            response_data = {'status' : 'success', 'message' : ''}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


#@login_required()
def submit_e_assignment_answer(request, course_id, assignment_id):
    response_data = {'status' : 'failed', 'message' : 'error submitting'}
    if request.is_ajax():
        if request.method == 'POST':
            # Extract parameters from post
            question_id = int(request.POST['question_id'])
            try:
                file = request.FILES["file"]
            except:
                response_data = {'status' : 'failed', 'message' : 'missing file'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        
            # Fetch from database
            course = Course.objects.get(id=course_id)
            student = Student.objects.get(user=request.user)
            assignment = Assignment.objects.get(assignment_id=assignment_id)

            # Fetch question and error if not found.
            try:
                question = EssayQuestion.objects.get(
                    assignment=assignment,
                    question_id=question_id,
                )
            except MultipleChoiceQuestion.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'cannot find question'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")

            try:
                submission = EssaySubmission.objects.get(
                    student=student,
                    question=question,
                )
            except EssaySubmission.DoesNotExist:
                submission = EssaySubmission.objects.create(
                    student=student,
                    question=question,
                )
            submission.file = file
            submission.save()
            response_data = {'status' : 'success', 'message' : 'submitted'}

#            form = EssaySubmissionForm(instance=submission, files=request.FILES)
#            if form.is_valid():
#                form.save()  # Save the form contents to the model
#                response_data = {'status' : 'success', 'message' : 'submitted'}
#            else:
#                response_data = {'status' : 'failed', 'message' : form.errors}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def submit_mc_assignment_answer(request, course_id, assignment_id):
    if request.is_ajax():
        if request.method == 'POST':
            # Extract parameters from post
            question_id = int(request.POST['question_id'])
            answer = request.POST['answer']
            
            # Fetch from database
            course = Course.objects.get(id=course_id)
            assignment = Assignment.objects.get(assignment_id=assignment_id)
            student = Student.objects.get(user=request.user)
            
            # Fetch question and error if not found.
            try:
                question = MultipleChoiceQuestion.objects.get(
                    assignment=assignment,
                    question_id=question_id,
                )
            except MultipleChoiceQuestion.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'cannot find question'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")

            # Fetch submission and create new submission if not found.
            try:
                submission = MultipleChoiceSubmission.objects.get(
                    student=student,
                    question=question,
                )
            except MultipleChoiceSubmission.DoesNotExist:
                submission = MultipleChoiceSubmission.objects.create(
                    student=student,
                    question=question,
                )

            # Process answer
            if answer == 'A':
                submission.a = not submission.a
            if answer == 'B':
                submission.b = not submission.b
            if answer == 'C':
                submission.c = not submission.c
            if answer == 'D':
                submission.d = not submission.d
            if answer == 'E':
                submission.e = not submission.e
            if answer == 'F':
                submission.f = not submission.f
            submission.save()
    
            # Return success results
            response_data = {'status' : 'success', 'message' : ''}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

    response_data = {'status' : 'failed', 'message' : 'error submitting'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def submit_tf_assignment_answer(request, course_id, assignment_id):
    if request.is_ajax():
        if request.method == 'POST':
            # Extract parameters from post
            question_id = int(request.POST['question_id'])
            answer = request.POST['answer']
            
            # Fetch from database
            course = Course.objects.get(id=course_id)
            assignment = Assignment.objects.get(assignment_id=assignment_id)
            student = Student.objects.get(user=request.user)

            # Fetch question and error if not found.
            try:
                question = TrueFalseQuestion.objects.get(
                    assignment=assignment,
                    question_id=question_id,
                )
            except MultipleChoiceQuestion.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'cannot find question'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")

            # Fetch submission and create new submission if not found.
            try:
                submission = TrueFalseSubmission.objects.get(
                    student=student,
                    question_id=question_id,
                )
            except TrueFalseSubmission.DoesNotExist:
                submission = TrueFalseSubmission.objects.create(
                    student=student,
                    question_id=question_id,
                )

            # Process the answer
            # Return success results
            submission.answer = answer == "true"
            submission.save()

            response_data = {'status' : 'success', 'message' : 'submitted'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def submit_r_assignment_answer(request, course_id, assignment_id):
    if request.is_ajax():
        if request.method == 'POST':
            # Extract parameters from post
            question_id = int(request.POST['question_id'])
            answer = request.POST['answer']
            
            # Fetch from database
            course = Course.objects.get(id=course_id)
            assignment = Assignment.objects.get(assignment_id=assignment_id)
            student = Student.objects.get(user=request.user)
            
            # Fetch question and error if not found.
            try:
                question = ResponseQuestion.objects.get(
                    assignment=assignment,
                    question_id=question_id,
                )
            except ResponseQuestion.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'cannot find question'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        
            # Fetch submission and create new submission if not found.
            try:
                submission = ResponseSubmission.objects.get(
                    student=student,
                    question_id=question_id,
                )
            except ResponseSubmission.DoesNotExist:
                submission = ResponseSubmission.objects.create(
                    student=student,
                    question_id=question_id,
                )
        
            # Process the answer
            # Return success results
            submission.answer = answer
            submission.save()
            
            response_data = {'status' : 'success', 'message' : 'submitted'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def submit_assignment(request, course_id, assignment_id):
    if request.is_ajax():
        if request.method == 'POST':
            # Fetch from database
            course = Course.objects.get(id=course_id)
            assignment = Assignment.objects.get(assignment_id=assignment_id)
            student = Student.objects.get(user=request.user)

            # Fetch submission and create new submission if not found.
            try:
                submission = AssignmentSubmission.objects.get(
                    student=student,
                    assignment=assignment,
                )
            except AssignmentSubmission.DoesNotExist:
                submission = AssignmentSubmission.objects.create(
                    student=student,
                    assignment=assignment,
                )
            submission.is_finished = True
            submission.save()
            response_data = {'status' : 'success', 'message' : 'submitted'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
