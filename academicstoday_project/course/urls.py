from django.conf.urls import patterns, include, url

from . import views

# Import custom views.
from course.views import course

urlpatterns = patterns('',
    # Announcement
    url(r'^course/(\d)/$', course.course),
    url(r'^course/(\d)/home$', course.course_home),
  
    # Syllabus
    url(r'^course/(\d)/syllabus$', course.course_syllabus),
   
    # Grades & Policy
    url(r'^course/(\d)/policy$', course.course_policy),

    # Lecture
    url(r'^course/(\d)/lectures$', course.course_lectures),
    url(r'^course/(\d)/lecture$', course.lecture),
                       
    # Assignment
    url(r'^course/(\d)/assignments$', course.assignments),
    url(r'^course/(\d)/assignment_delete$', course.assignment_delete),
    url(r'^course/(\d)/assignment_essay$', course.assignment_essay),
    url(r'^course/(\d)/assignment_multiplechoice$', course.assignment_multiplechoice),
    url(r'^course/(\d)/assignment_truefalse$', course.assignment_truefalse),
    url(r'^course/(\d)/assignment_response$', course.assignment_response),
    url(r'^course/(\d)/upload_essay_assignment$', course.upload_essay_assignment),
    url(r'^course/(\d)/submit_mc_assignment_answer$', course.submit_mc_assignment_answer),
    url(r'^course/(\d)/submit_truefalse_assignment_answer$', course.submit_truefalse_assignment_answer),
    url(r'^course/(\d)/submit_response_assignment_answer$', course.submit_response_assignment_answer),
    url(r'^course/(\d)/submit_mc_assignment_completion$', course.submit_mc_assignment_completion),
    url(r'^course/(\d)/submit_truefalse_assignment_completion$', course.submit_truefalse_assignment_completion),
    url(r'^course/(\d)/submit_response_assignment_completion$', course.submit_response_assignment_completion),
                       
    # Quiz
    url(r'^course/(\d)/quizzes$', course.course_quizzes),
    url(r'^course/(\d)/quiz_truefalse$', course.quiz_truefalse),
    url(r'^course/(\d)/submit_truefalse_quiz_answer$', course.submit_truefalse_quiz_answer),
    url(r'^course/(\d)/submit_truefalse_quiz_completion$', course.submit_truefalse_quiz_completion),
    url(r'^course/(\d)/quiz_delete$', course.quiz_delete),
    
    # Exam
    url(r'^course/(\d)/exams$', course.course_exams),
    url(r'^course/(\d)/exam_multiplechoice$', course.exam_multiplechoice),
    url(r'^course/(\d)/submit_mc_exam_answer$', course.submit_mc_exam_answer),
    url(r'^course/(\d)/submit_mc_exam_completion$', course.submit_mc_exam_completion),
    url(r'^course/(\d)/exam_delete$', course.exam_delete),
                       
    # Discussion
    url(r'^course/(\d)/discussion$', course.course_discussion),
)