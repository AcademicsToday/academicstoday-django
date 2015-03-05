from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from registrar.models import Course
from course.models import TrueFalseQuestion
from course.models import TrueFalseSubmission
from course.models import Quiz
from course.models import QuizSubmission
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
def quizzes_page(request, course_id):
    course = Course.objects.get(id=course_id)
    
    # Fetch all the quizzes for this course.
    try:
        quizzes = Quiz.objects.filter(course_id=course_id).order_by('order_num')
    except Quiz.DoesNotExist:
        quizzes = None

    # Fetch all submitted quizzes
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

    return render(request, 'quiz/list.html',{
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
        'local_css_urls' : settings.SB_ADMIN_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_JS_LIBRARY_URLS,
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
    
    return render(request, 'quiz/truefalse_modal.html',{
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
