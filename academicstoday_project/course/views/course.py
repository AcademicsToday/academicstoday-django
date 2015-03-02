from django.shortcuts import render
from django.core import serializers
from registrar.models import Course
from registrar.models import CourseEnrollment
from course.models import Announcement
from course.models import Syllabus
from course.models import Policy
from course.models import Week
from course.models import Lecture
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
from course.models import Quiz
from course.models import QuizSubmission
import json
import datetime
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings


# Forms
from course.forms import EssaySubmissionForm
from course.forms import AssignmentSubmissionForm


# Developer Notes:
# (1) Templates
# https://docs.djangoproject.com/en/1.7/ref/templates
#
# (2) JSON
# https://docs.djangoproject.com/en/1.7/topics/serialization/



css_library_urls = ["js/jquery/1.11.1/jquery-ui.css",
                    "js/bootstrap/3.3.2/css/bootstrap.min.css",
                    "js/font-awesome/4.2.0/css/font-awesome.css",
                    "js/font-awesome/4.2.0/css/font-awesome.min.css",
                    "css/sb-admin.css"]

js_library_urls = ["js/jquery/1.11.1/jquery.min.js",
                   "js/jquery/1.11.1/jquery.tablesorter.js",
                   "js/jquery/1.11.1/jquery-ui.js",
                   "js/jquery-easing/1.3/jquery.easing.min.js",
                   "js/bootstrap/3.3.2/js/bootstrap.min.js",
                   "js/bootstrap/3.3.2/js/bootstrap.js",
#                            "js/morris/0.5.0/morris.js",
#                            "js/morris/0.5.0/morris.min.js",
                   "js/morris/0.5.0/raphael.min.js",
#                            "js/morris/0.5.0/morris-data.js",
#                            "js/flot/x.x/excanvas.min.js",
#                            "js/flot/x.x/flot-data.js",
#                            "js/flot/x.x/jquery.flot.js",
#                            "js/flot/x.x/jquery.flot.pie.js",
#                            "js/flot/x.x/jquery.flot.resize.js",
#                            "js/flot/x.x/jquery.flot.tooltip.min.js",
                            ]

def logout_authentication(request):
    response_data = {'status' : 'success', 'message' : 'Done'}
    if request.is_ajax():
        if request.method == 'POST':
            logout(request)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def course(request, course_id, tab):
    course = Course.objects.get(id=course_id)
    return render(request, 'course/announcement/list.html',{
        'course' : course,
        'user' : request.user,
        'tab' : tab,
        'local_css_urls' : css_library_urls,
        'local_js_urls' : js_library_urls
    })


@login_required(login_url='/landpage')
def course_home(request, course_id):
    course = Course.objects.get(id=course_id)
    try:
        announcements = Announcement.objects.filter(course_id=course_id).order_by('-post_date')
    except Announcement.DoesNotExist:
        announcements = None
    return render(request, 'course/announcement/list.html',{
        'course' : course,
        'announcements' : announcements,
        'user' : request.user,
        'tab' : 'home',
        'local_css_urls' : css_library_urls,
        'local_js_urls' : js_library_urls
    })


@login_required(login_url='/landpage')
def course_syllabus(request, course_id):
    course = Course.objects.get(id=course_id)
    try:
        syllabus = Syllabus.objects.get(course_id=course_id)
    except Syllabus.DoesNotExist:
        syllabus = None
    return render(request, 'course/syllabus/view.html',{
        'course' : course,
        'syllabus' : syllabus,
        'user' : request.user,
        'tab' : 'syllabus',
        'local_css_urls' : css_library_urls,
        'local_js_urls' : js_library_urls
    })


@login_required(login_url='/landpage')
def course_policy(request, course_id):
    course = Course.objects.get(id=course_id)
    try:
        policy = Policy.objects.get(course_id=course_id)
    except Policy.DoesNotExist:
        policy = None
    return render(request, 'course/policy/view.html',{
        'course' : course,
        'user' : request.user,
        'policy' : policy,
        'tab' : 'policy',
        'local_css_urls' : css_library_urls,
        'local_js_urls' : js_library_urls
    })


@login_required(login_url='/landpage')
def course_lectures(request, course_id):
    course = Course.objects.get(id=course_id)
    try:
        weeks = Week.objects.filter(course_id=course_id)
    except Week.DoesNotExist:
        weeks = None
    try:
        lectures = Lecture.objects.filter(course_id=course_id).order_by('-lecture_num')
    except Lecture.DoesNotExist:
        lectures = None
    return render(request, 'course/lecture/list.html',{
        'course' : course,
        'weeks' : weeks,
        'lectures' : lectures,
        'user' : request.user,
        'tab' : 'lectures',
        'local_css_urls' : css_library_urls,
        'local_js_urls' : js_library_urls
    })


@login_required(login_url='/landpage')
def lecture(request, course_id):
    response_data = {}
    if request.is_ajax():
         if request.method == 'POST':
             # Check to see if any fields where missing from the form.
             if request.POST['lecture_id'] != '':
                 try:
                     lecture_id = request.POST['lecture_id']
                     lecture = Lecture.objects.get(id=lecture_id)
                 except Lecture.DoesNotExist:
                     lecture = None
                 return render(request, 'course/lecture/details.html',{
                    'lecture' : lecture,
                    'user' : request.user,
                    'local_css_urls' : css_library_urls,
                    'local_js_urls' : js_library_urls
                 })


@login_required(login_url='/landpage')
def assignments(request, course_id):
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

    return render(request, 'course/assignment/list.html',{
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
        'local_css_urls' : css_library_urls,
        'local_js_urls' : js_library_urls
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
                    ).delete()
                    response_data = {'status' : 'success', 'message' : 'assignment was deleted'}
                except EssaySubmission.DoesNotExist:
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
                except EssaySubmission.DoesNotExist:
                    response_data = {'status' : 'failed', 'message' : 'assignment not found'}
            elif assignment_type == settings.RESPONSE_ASSIGNMENT_TYPE:
                try:
                    ResponseSubmission.objects.filter(
                        assignment_id=assignment_id,
                        student_id=student_id,
                        course_id=course_id,
                    ).delete()
                    response_data = {'status' : 'success', 'message' : 'assignment was deleted'}
                except EssaySubmission.DoesNotExist:
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

            return render(request, 'course/assignment/essay_modal.html',{
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
                    course_id=course_id
                )
            except MultipleChoiceQuestion.DoesNotExist:
                questions = None
        
            return render(request, 'course/assignment/mc_modal.html',{
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
        course_id=int(request.POST['course_id'])
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
                )
            except MultipleChoiceSubmission.DoesNotExist:
                submission = MultipleChoiceSubmission.create(
                    student_id=student_id,
                    assignment_id=assignment_id,
                    course_id=course_id,
                    question_num=question_num,
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

            return render(request, 'course/assignment/truefalse_modal.html',{
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
        
            return render(request, 'course/assignment/response_modal.html',{
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


@login_required(login_url='/landpage')
def course_quizzes(request, course_id):
    course = Course.objects.get(id=course_id)
    
    # Fetch all the assignments for this course.
    try:
        quizzes = Quiz.objects.filter(course_id=course_id).order_by('order_num')
    except Assignment.DoesNotExist:
        quizzes = None

    # Fetch all submitted assignments
    try:
        submitted_quizzes = QuizSubmission.objects.filter(course_id=course_id,
                                                          student_id=request.user.id)
    except QuizSubmission.DoesNotExist:
        submitted_quizzes = None

    # If the submissions & quizzes counts do not equal, then we have to
    # iterate through all the quizzes and create the missing 'submission'
    # entries for our system.
    if len(quizzes) != len(submitted_quizzes):
        for quiz in quizzes:
            found_quiz = False
            for submitted_quiz in submitted_quizzes:
                if quiz.id == submitted_quiz.quiz_id:
                    found_quiz = True
            if not found_quiz:
                submission = QuizSubmission.create(
                    student_id=request.user.id,
                    course_id=course_id,
                    quiz_id=quiz.id,
                    type=quiz.type,
                    order_num=quiz.order_num
                )
                submission.save()

    return render(request, 'course/quiz/list.html',{
        'course' : course,
        'user' : request.user,
        'quizzes' : quizzes,
        'submitted_quizzes' : submitted_quizzes,
        'ESSAY_ASSIGNMENT_TYPE' : settings.ESSAY_ASSIGNMENT_TYPE,
        'MULTIPLECHOICE_ASSIGNMENT_TYPE' : settings.MULTIPLECHOICE_ASSIGNMENT_TYPE,
        'TRUEFALSE_ASSIGNMENT_TYPE' : settings.TRUEFALSE_ASSIGNMENT_TYPE,
        'RESPONSE_ASSIGNMENT_TYPE' : settings.RESPONSE_ASSIGNMENT_TYPE,
        'tab' : 'quizzes',
        'subtab' : '',
        'local_css_urls' : css_library_urls,
        'local_js_urls' : js_library_urls,
    })


@login_required()
def quiz_truefalse(request, course_id):
    if request.is_ajax():
        if request.method == 'POST':
            student_id = int(request.POST['student_id'])
            quiz_id = int(request.POST['quiz_id'])
            quiz = Quiz.objects.get(id=quiz_id)
            
            # Fetch questions
            try:
                questions = TrueFalseQuestion.objects.filter(
                    assignment_id=0,
                    course_id=course_id,
                    quiz_id=quiz.id,
                )
            except TrueFalseQuestion.DoesNotExist:
                questions = None
        
            # Fetch submissions
            try:
                submissions = TrueFalseSubmission.objects.filter(
                    student_id=student_id,
                    assignment_id=0,
                    course_id=course_id,
                    quiz_id=quiz.id,
                )
            except TrueFalseSubmission.DoesNotExist:
                submission = None
    
    return render(request, 'course/quiz/truefalse_modal.html',{
        'quiz' : quiz,
        'questions' : questions,
        'submissions' : submissions,
    })


@login_required()
def submit_truefalse_quiz_answer(request, course_id):
    if request.is_ajax():
        if request.method == 'POST':
            quiz_id = int(request.POST['quiz_id'])
            student_id = int(request.POST['student_id'])
            course_id = int(request.POST['course_id'])
            question_num = int(request.POST['question_num'])
            key = request.POST['key']
            
            # Fetch submission and create new submission if not found.
            try:
                submission = TrueFalseSubmission.objects.get(
                    student_id=student_id,
                    assignment_id=0,
                    course_id=course_id,
                    question_num=question_num,
                    quiz_id=quiz_id,
                )
            except TrueFalseSubmission.DoesNotExist:
                submission = TrueFalseSubmission.create(
                student_id=student_id,
                assignment_id=0,
                course_id=course_id,
                question_num=question_num,
                quiz_id=quiz_id,
            )
            
            # Save answer
            submission.answer = key == "true"
            submission.save()
            
            response_data = {'status' : 'success', 'message' : 'submitted'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    response_data = {'status' : 'failed', 'message' : 'error submitting'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def submit_truefalse_quiz_completion(request, course_id):
    # Update the 'submission_date' of our entry to indicate we
    # have finished the quiz.
    submission = QuizSubmission.objects.get(
        quiz_id=int(request.POST['quiz_id']),
        student_id=int(request.POST['student_id']),
        course_id=int(request.POST['course_id']),
    )
    submission.submission_date = datetime.datetime.utcnow()
    submission.save()
                                                  
    response_data = {'status' : 'success', 'message' : ''}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def quiz_delete(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'quiz was not deleted'}
    if request.is_ajax():
        if request.method == 'POST':
            student_id = int(request.POST['student_id'])
            quiz_id = int(request.POST['quiz_id'])
            quiz_type = int(request.POST['quiz_type'])
            
            # Update the 'submission_date' of our entry to indicate we
            # have finished the quiz.
            submission = QuizSubmission.objects.get(
                quiz_id=int(request.POST['quiz_id']),
                student_id=int(request.POST['student_id']),
                course_id=int(request.POST['course_id'])
            )
            submission.submission_date = None
            submission.save()
                                                          
            # Delete quiz depending on what type
            if quiz_type == settings.TRUEFALSE_ASSIGNMENT_TYPE:
                try:
                    TrueFalseSubmission.objects.get(
                        assignment_id=0,
                        student_id=student_id,
                        course_id=course_id,
                        quiz_id=quiz_id,
                    ).delete()
                                                                      
                    # Send JSON Response indicating success
                    response_data = {'status' : 'success', 'message' : 'assignment was deleted'}
                except EssaySubmission.DoesNotExist:
                    response_data = {'status' : 'failed', 'message' : 'assignment not found'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def course_exams(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'course/exam/exams.html',{
        'course' : course,
        'user' : request.user,
        'tab' : 'exams',
        'local_css_urls' : css_library_urls,
        'local_js_urls' : js_library_urls
    })


@login_required(login_url='/landpage')
def course_discussion(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'course/discussion/discussion.html',{
        'course' : course,
        'user' : request.user,
        'tab' : 'discussion',
        'local_css_urls' : css_library_urls,
        'local_js_urls' : js_library_urls
    })
