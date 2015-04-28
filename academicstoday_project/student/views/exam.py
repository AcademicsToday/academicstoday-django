from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

from registrar.models import Course
from registrar.models import Student
from registrar.models import MultipleChoiceQuestion
from registrar.models import MultipleChoiceSubmission
from registrar.models import Exam
from registrar.models import ExamSubmission
import json
import datetime

# Forms
from student.forms import EssaySubmissionForm
from student.forms import AssignmentSubmissionForm


# Private


def get_submitted_exams(course, student):
    # Fetch all the assignments for this course.
    try:
        exams = Exam.objects.filter(course=course).order_by('exam_num')
    except Exam.DoesNotExist:
        exams = None

    # Fetch all submitted assignments
    try:
        submitted_exams = ExamSubmission.objects.filter(
            exam__course=course,
            student=student
        )
    except ExamSubmission.DoesNotExist:
        submitted_exams = None
    
    # If the submissions & quizzes counts do not equal, then we have to
    # iterate through all the quizzes and create the missing 'submission'
    # entries for our system.
    if len(exams) != len(submitted_exams):
        for exam in exams:
            found_exam = False
            for submitted_exam in submitted_exams:
                if exam.id == submitted_exam.exam_id:
                    found_exam = True
            if not found_exam:
                submission = ExamSubmission.objects.create(
                    student=student,
                    exam=exam,
                )
                submission.save()
        submitted_exams = ExamSubmission.objects.filter(
            exam__course=course,
            student=student
        )
    return submitted_exams


# Public


@login_required(login_url='/landpage')
def exams_page(request, course_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user)
    return render(request, 'course/exam/exams_view.html',{
        'course' : course,
        'user' : request.user,
        'submitted_exams' : get_submitted_exams(course, student),
        'ESSAY_QUESTION_TYPE' : settings.ESSAY_QUESTION_TYPE,
        'MULTIPLECHOICE_QUESTION_TYPE' : settings.MULTIPLECHOICE_QUESTION_TYPE,
        'TRUEFALSE_QUESTION_TYPE' : settings.TRUEFALSE_QUESTION_TYPE,
        'RESPONSE_QUESTION_TYPE' : settings.RESPONSE_QUESTION_TYPE,
        'tab' : 'exams',
        'subtab' : '',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


@login_required(login_url='/landpage')
def exams_table(request, course_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user)
    return render(request, 'course/exam/exams_table.html',{
        'course' : course,
        'user' : request.user,
        'submitted_exams' : get_submitted_exams(course, student),
        'ESSAY_QUESTION_TYPE' : settings.ESSAY_QUESTION_TYPE,
        'MULTIPLECHOICE_QUESTION_TYPE' : settings.MULTIPLECHOICE_QUESTION_TYPE,
        'TRUEFALSE_QUESTION_TYPE' : settings.TRUEFALSE_QUESTION_TYPE,
        'RESPONSE_QUESTION_TYPE' : settings.RESPONSE_QUESTION_TYPE,
    })


@login_required()
def delete_exam(request, course_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deletion'}
    if request.is_ajax():
        if request.method == 'POST':
            exam_id = int(request.POST['exam_id'])
            course = Course.objects.get(id=course_id)
            student = Student.objects.get(user=request.user)
            exam = Exam.objects.get(exam_id=exam_id)
            
            # Set 'is_finished' to false to indicate we need to take the
            # exam all over.
            try:
                submission = ExamSubmission.objects.get(
                    student=student,
                    exam=exam,
                )
                submission.is_finished = False
                submission.save()
            except ExamSubmission.DoesNotExist:
                return HttpResponse(json.dumps({
                    'status' : 'failed', 'message' : 'record does not exist'
                }), content_type="application/json")
                                                    
            # Delete all previous entries.
            try:
                 MultipleChoiceSubmission.objects.filter(
                    question__exam=exam,
                    student=student
                ).delete()
            except MultipleChoiceSubmission.DoesNotExist:
                pass
            response_data = {'status' : 'success', 'message' : 'exam was deleted'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")



@login_required(login_url='/landpage')
def exam_page(request, course_id, exam_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user)
    exam = Exam.objects.get(exam_id=exam_id)
    
    # Load all multiple-choice type questions/submissions for this assignment.
    try:
        mc_questions = MultipleChoiceQuestion.objects.filter(exam=exam).order_by('question_num')
    except MultipleChoiceQuestion.DoesNotExist:
        mc_questions = None
    try:
        mc_submissions = MultipleChoiceSubmission.objects.filter(question__exam=exam, student=student)
    except MultipleChoiceSubmission.DoesNotExist:
        mc_submissions = None
    
    return render(request, 'course/exam/question_view.html',{
        'student': student,
        'course': course,
        'exam': exam,
        'mc_questions': mc_questions,
        'mc_submissions': mc_submissions,
        'ESSAY_QUESTION_TYPE': settings.ESSAY_QUESTION_TYPE,
        'MULTIPLECHOICE_QUESTION_TYPE': settings.MULTIPLECHOICE_QUESTION_TYPE,
        'TRUEFALSE_QUESTION_TYPE': settings.TRUEFALSE_QUESTION_TYPE,
        'RESPONSE_QUESTION_TYPE': settings.RESPONSE_QUESTION_TYPE,
        'user': request.user,
        'tab': 'assignment',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS,
    })


@login_required()
def submit_mc_exam_answer(request, course_id, exam_id):
    response_data = {'status' : 'failed', 'message' : 'error submitting'}
    if request.is_ajax():
        if request.method == 'POST':
            # Extract parameters from post
            question_id = int(request.POST['question_id'])
            answer = request.POST['answer']
            
            # Fetch from database
            course = Course.objects.get(id=course_id)
            exam = Exam.objects.get(exam_id=exam_id)
            student = Student.objects.get(user=request.user)
            
            # Fetch question and error if not found.
            try:
                question = MultipleChoiceQuestion.objects.get(
                    exam=exam,
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

            # Save Answer
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
            
            # Caclulate score
            total = 6
            correct = 0
            if submission.a == submission.question.a_is_correct:
                correct += 1;
            if submission.b == submission.question.b_is_correct:
                correct += 1;
            if submission.c == submission.question.c_is_correct:
                correct += 1;
            if submission.d == submission.question.d_is_correct:
                correct += 1;
            if submission.e == submission.question.e_is_correct:
                correct += 1;
            if submission.f == submission.question.f_is_correct:
                correct += 1;
            
            # If all choices have been correctly selected, then give full credit.
            if total == correct:
                submission.marks = submission.question.marks
            else:
                submission.marks = 0
            submission.save()
                
            # Return success results
            response_data = {'status' : 'success', 'message' : 'submitted'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def submit_exam(request, course_id, exam_id):
    if request.is_ajax():
        if request.method == 'POST':
            # Fetch from database
            course = Course.objects.get(id=course_id)
            exam = Exam.objects.get(exam_id=exam_id)
            student = Student.objects.get(user=request.user)
            
            # Fetch submission and create new submission if not found.
            try:
                submission = ExamSubmission.objects.get(
                    student=student,
                    exam=exam,
                )
            except ExamSubmission.DoesNotExist:
                submission = ExamSubmission.objects.create(
                    student=student,
                    exam=exam,
                )
            submission.is_finished = True
            submission.save()
            
            # Compute Exam Score
            compute_score(submission)
            
            response_data = {'status' : 'success', 'message' : 'submitted'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


#-------------------#
# Private Functions #
#-------------------#

def compute_score(submission):
    submission.total_marks = 0
    submission.earned_marks = 0
    
    # Multiple Choice Submission(s)
    mc_submissions = MultipleChoiceSubmission.objects.filter(
        student=submission.student,
        question__exam=submission.exam,
    )
    for mc_submission in mc_submissions:
        submission.total_marks += mc_submission.question.marks
        submission.earned_marks += mc_submission.marks

    # Compute Percent
    try:
        submission.percent = round((submission.earned_marks / submission.total_marks) * 100)
    except ZeroDivisionError:
        submission.percent = 0

    # Save calculation
    submission.save()
