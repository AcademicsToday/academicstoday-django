from django.conf.urls import patterns, include, url

from . import views

# Import custom views.
from course.views import announcement
from course.views import syllabus
from course.views import policy
from course.views import lecture
from course.views import assignment
from course.views import quiz
from course.views import exam
from course.views import discussion

urlpatterns = patterns('',
    # Announcement
    url(r'^course/(\d)/$', announcement.course),
    url(r'^course/(\d)/home$', announcement.course_home),
  
    # Syllabus
    url(r'^course/(\d)/syllabus$', syllabus.course_syllabus),
   
    # Grades & Policy
    url(r'^course/(\d)/policy$', policy.course_policy),

    # Lecture
    url(r'^course/(\d)/lectures$', lecture.course_lectures),
    url(r'^course/(\d)/lecture$', lecture.lecture),
                       
    # Assignment
    url(r'^course/(\d)/assignments$', assignment.assignments),
    url(r'^course/(\d)/assignment_delete$', assignment.assignment_delete),
    url(r'^course/(\d)/assignment_essay$', assignment.assignment_essay),
    url(r'^course/(\d)/assignment_multiplechoice$', assignment.assignment_multiplechoice),
    url(r'^course/(\d)/assignment_truefalse$', assignment.assignment_truefalse),
    url(r'^course/(\d)/assignment_response$', assignment.assignment_response),
    url(r'^course/(\d)/upload_essay_assignment$', assignment.upload_essay_assignment),
    url(r'^course/(\d)/submit_mc_assignment_answer$', assignment.submit_mc_assignment_answer),
    url(r'^course/(\d)/submit_truefalse_assignment_answer$', assignment.submit_truefalse_assignment_answer),
    url(r'^course/(\d)/submit_response_assignment_answer$', assignment.submit_response_assignment_answer),
    url(r'^course/(\d)/submit_mc_assignment_completion$', assignment.submit_mc_assignment_completion),
    url(r'^course/(\d)/submit_truefalse_assignment_completion$', assignment.submit_truefalse_assignment_completion),
    url(r'^course/(\d)/submit_response_assignment_completion$', assignment.submit_response_assignment_completion),
                       
    # Quiz
    url(r'^course/(\d)/quizzes$', quiz.course_quizzes),
    url(r'^course/(\d)/quiz_truefalse$', quiz.quiz_truefalse),
    url(r'^course/(\d)/submit_truefalse_quiz_answer$', quiz.submit_truefalse_quiz_answer),
    url(r'^course/(\d)/submit_truefalse_quiz_completion$', quiz.submit_truefalse_quiz_completion),
    url(r'^course/(\d)/quiz_delete$', quiz.quiz_delete),
    
    # Exam
    url(r'^course/(\d)/exams$', exam.course_exams),
    url(r'^course/(\d)/exam_multiplechoice$', exam.exam_multiplechoice),
    url(r'^course/(\d)/submit_mc_exam_answer$', exam.submit_mc_exam_answer),
    url(r'^course/(\d)/submit_mc_exam_completion$', exam.submit_mc_exam_completion),
    url(r'^course/(\d)/exam_delete$', exam.exam_delete),
                       
    # Discussion
    url(r'^course/(\d)/discussion$', discussion.course_discussion),
)