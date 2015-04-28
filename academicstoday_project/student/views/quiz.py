from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from registrar.models import Course
from registrar.models import Student
from registrar.models import TrueFalseQuestion
from registrar.models import TrueFalseSubmission
from registrar.models import Quiz
from registrar.models import QuizSubmission
import json
import datetime


# Private


def get_submitted_quizzes(course, student):
    # Fetch all the quizzes for this course.
    try:
        quizzes = Quiz.objects.filter(course=course).order_by('quiz_num')
    except Quiz.DoesNotExist:
        quizzes = None

    # Fetch all submitted quizzes
    try:
        submitted_quizzes = QuizSubmission.objects.filter(
            quiz__course=course,
            student=student
        )
    except QuizSubmission.DoesNotExist:
        submitted_quizzes = None
    
    # If the submissions & quizzes counts do not equal, then we have to
    # iterate through all the quizzes and create the missing 'submission'
    # entries for our system.
    if len(quizzes) != len(submitted_quizzes):
        for quiz in quizzes:
            found_quiz = False
            for submitted_quiz in submitted_quizzes:
                if quiz == submitted_quiz:
                    found_quiz = True
            if not found_quiz:
                submission = QuizSubmission.objects.create(
                    student=student,
                    quiz=quiz,
                )
                submission.save()
        submitted_quizzes = QuizSubmission.objects.filter(
            quiz__course=course,
            student=student
        )
    return submitted_quizzes

# Public


@login_required(login_url='/landpage')
def quizzes_page(request, course_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user)
    return render(request, 'course/quiz/quizzes_view.html',{
        'course' : course,
        'user' : request.user,
        'submitted_quizzes' : get_submitted_quizzes(course, student),
        'ESSAY_QUESTION_TYPE' : settings.ESSAY_QUESTION_TYPE,
        'MULTIPLECHOICE_QUESTION_TYPE' : settings.MULTIPLECHOICE_QUESTION_TYPE,
        'TRUEFALSE_QUESTION_TYPE' : settings.TRUEFALSE_QUESTION_TYPE,
        'RESPONSE_QUESTION_TYPE' : settings.RESPONSE_QUESTION_TYPE,
        'tab' : 'quizzes',
        'subtab' : '',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def quizzes_table(request, course_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user)
    return render(request, 'course/quiz/quizzes_table.html',{
        'course' : course,
        'user' : request.user,
        'submitted_quizzes' : get_submitted_quizzes(course, student),
        'ESSAY_QUESTION_TYPE' : settings.ESSAY_QUESTION_TYPE,
        'MULTIPLECHOICE_QUESTION_TYPE' : settings.MULTIPLECHOICE_QUESTION_TYPE,
        'TRUEFALSE_QUESTION_TYPE' : settings.TRUEFALSE_QUESTION_TYPE,
        'RESPONSE_QUESTION_TYPE' : settings.RESPONSE_QUESTION_TYPE,
    })


@login_required()
def delete_quiz(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deletion'}
    if request.is_ajax():
        if request.method == 'POST':
            quiz_id = int(request.POST['quiz_id'])
            course = Course.objects.get(id=course_id)
            student = Student.objects.get(user=request.user)
            quiz = Quiz.objects.get(quiz_id=quiz_id)
            
            # Set 'is_finished' to false to indicate we need to take the
            # assignment all over.
            try:
                submission = QuizSubmission.objects.get(
                    student=student,
                    quiz=quiz,
                )
                submission.is_finished = False
                submission.save()
            except QuizSubmission.DoesNotExist:
                return HttpResponse(json.dumps({
                    'status' : 'failed',
                    'message' : 'record does not exist'
                }), content_type="application/json")
                                                          
            # Delete all previous entries.
            try:
                tf_submissions = TrueFalseSubmission.objects.filter(question__quiz=quiz, student=student)
                tf_submissions.delete()
            except TrueFalseSubmission.DoesNotExist:
                pass
            response_data = {'status' : 'success', 'message' : 'deleted'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url='/landpage')
def quiz_page(request, course_id, quiz_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user)
    quiz = Quiz.objects.get(quiz_id=quiz_id)
    
    # Load all true/false type questions/submissions for this assignment.
    try:
        tf_questions = TrueFalseQuestion.objects.filter(quiz=quiz).order_by('question_num')
    except TrueFalseQuestion.DoesNotExist:
        tf_questions = None
    try:
        tf_submissions = TrueFalseSubmission.objects.filter(question__quiz=quiz, student=student)
    except tf_submissions.DoesNotExist:
        tf_submissions = None
    
    return render(request, 'course/quiz/question_view.html',{
        'course' : course,
        'student': student,
        'user' : request.user,
        'quiz' : quiz,
        'tf_questions': tf_questions,
        'tf_submissions': tf_submissions,
        'ESSAY_QUESTION_TYPE' : settings.ESSAY_QUESTION_TYPE,
        'MULTIPLECHOICE_QUESTION_TYPE' : settings.MULTIPLECHOICE_QUESTION_TYPE,
        'TRUEFALSE_QUESTION_TYPE' : settings.TRUEFALSE_QUESTION_TYPE,
        'RESPONSE_QUESTION_TYPE' : settings.RESPONSE_QUESTION_TYPE,
        'tab' : 'quiz',
        'subtab' : '',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


@login_required()
def submit_tf_assignment_answer(request, course_id, quiz_id):
    if request.is_ajax():
        if request.method == 'POST':
            # Extract parameters from post
            question_id = int(request.POST['question_id'])
            answer = request.POST['answer']
            
            # Fetch from database
            course = Course.objects.get(id=course_id)
            quiz = Quiz.objects.get(quiz_id=quiz_id)
            student = Student.objects.get(user=request.user)
            
            # Fetch question and error if not found.
            try:
                question = TrueFalseQuestion.objects.get(
                    quiz=quiz,
                    question_id=question_id,
                )
            except TrueFalseQuestion.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'cannot find question'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        
            # Fetch submission and create new submission if not found.
            try:
                submission = TrueFalseSubmission.objects.get(
                    student=student,
                    question=question,
                )
            except TrueFalseSubmission.DoesNotExist:
                submission = TrueFalseSubmission.objects.create(
                    student=student,
                    question=question,
                )
            
            # Save answer
            submission.answer = answer == "true"
            submission.save()
            
            # Calculate the marks
            if submission.answer == submission.question.answer:
                submission.marks = submission.question.marks
            else:
                submission.marks = 0
            submission.save()
            
            # Return results
            response_data = {'status' : 'success', 'message' : 'submitted'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def submit_quiz(request, course_id, quiz_id):
    if request.is_ajax():
        if request.method == 'POST':
            # Fetch from database
            course = Course.objects.get(id=course_id)
            quiz = Quiz.objects.get(quiz_id=quiz_id)
            student = Student.objects.get(user=request.user)
            
            # Fetch submission and create new submission if not found.
            try:
                submission = QuizSubmission.objects.get(
                    student=student,
                    quiz=quiz,
                )
            except QuizSubmission.DoesNotExist:
                submission = QuizSubmission.objects.create(
                    student=student,
                    quiz=quiz,
                )
            submission.is_finished = True
            submission.save()
            
            # Process quiz score.
            compute_score(submission)
            
            response_data = {'status' : 'success', 'message' : 'submitted'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


#-------------------#
# Private Functions #
#-------------------#

def compute_score(submission):
    student = submission.student
    submission.total_marks = 0
    submission.earned_marks = 0

    # True / False Submission(s)
    tf_submissions = TrueFalseSubmission.objects.filter(
        student=student,
        question__quiz=submission.quiz,
    )
    for tf_submission in tf_submissions:
        submission.total_marks += tf_submission.question.marks
        submission.earned_marks += tf_submission.marks

    # Compute Percent
    try:
        submission.percent = round((submission.earned_marks / submission.total_marks) * 100)
    except ZeroDivisionError:
        submission.percent = 0

    # Save calculation
    submission.save()
