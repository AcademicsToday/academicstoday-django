from django.conf.urls import patterns, include, url

from . import views

# Import custom views.
from student.views import announcement
from student.views import syllabus
from student.views import policy
from student.views import lecture
from student.views import lecture_note
from student.views import assignment
from student.views import quiz
from student.views import exam
from student.views import discussion
from student.views import peer_review
from student.views import credit

urlpatterns = patterns('',
    # Announcement
    url(r'^course/(\d+)/announcements$', announcement.announcements_page),

    # Syllabus
    url(r'^course/(\d+)/syllabus$', syllabus.syllabus_page),

    # Grades & Policy
    url(r'^course/(\d+)/policy$', policy.policy_page),

    # Lecture
    url(r'^course/(\d+)/lectures$', lecture.lectures_page),
    url(r'^course/(\d+)/lecture$', lecture.lecture),
                       
    # Lecture Notes
    url(r'^course/(\d+)/lecture/(\d+)/notes$', lecture_note.lecture_notes_page),
    url(r'^course/(\d+)/lecture/(\d+)/view_lecture_note$', lecture_note.view_lecture_note),

    # Assignment(s)
    url(r'^course/(\d+)/assignments$', assignment.assignments_page),
    url(r'^course/(\d+)/assignments_table$', assignment.assignments_table),
    url(r'^course/(\d+)/delete_assignment$', assignment.delete_assignment),
                       
    # Assignment
    url(r'^course/(\d+)/assignment/(\d+)$', assignment.assignment_page),
    url(r'^course/(\d+)/assignment/(\d+)/submit_assignment$', assignment.submit_assignment),
    url(r'^course/(\d+)/assignment/(\d+)/submit_e_assignment_answer$', assignment.submit_e_assignment_answer),
    url(r'^course/(\d+)/assignment/(\d+)/submit_mc_assignment_answer$', assignment.submit_mc_assignment_answer),
    url(r'^course/(\d+)/assignment/(\d+)/submit_tf_assignment_answer$', assignment.submit_tf_assignment_answer),
    url(r'^course/(\d+)/assignment/(\d+)/submit_r_assignment_answer$', assignment.submit_r_assignment_answer),
                       
    # Quiz(zes)
    url(r'^course/(\d+)/quizzes$', quiz.quizzes_page),
    url(r'^course/(\d+)/quizzes_table$', quiz.quizzes_table),
    url(r'^course/(\d+)/quiz_delete$', quiz.delete_quiz),
                       
    # Quiz
    url(r'^course/(\d+)/quiz/(\d+)$', quiz.quiz_page),
    url(r'^course/(\d+)/quiz/(\d+)/submit_quiz$', quiz.submit_quiz),
    url(r'^course/(\d+)/quiz/(\d+)/submit_tf_quiz_answer$', quiz.submit_tf_assignment_answer),

    # Exam(s)
    url(r'^course/(\d+)/exams$', exam.exams_page),
    url(r'^course/(\d+)/exams_table$', exam.exams_table),
    url(r'^course/(\d+)/delete_exam$', exam.delete_exam),
                       
    # Exam
    url(r'^course/(\d+)/exam/(\d+)$', exam.exam_page),
    url(r'^course/(\d+)/exam/(\d+)/submit_exam$', exam.submit_exam),
    url(r'^course/(\d+)/exam/(\d+)/submit_mc_exam_answer$', exam.submit_mc_exam_answer),

    # Peer-Review
    url(r'^course/(\d+)/peer_reviews$', peer_review.peer_reviews_page),
    url(r'^course/(\d+)/peer_review/(\d+)$', peer_review.assignment_page),
    url(r'^course/(\d+)/peer_review/(\d+)/peer_review_modal$', peer_review.peer_review_modal),
    url(r'^course/(\d+)/peer_review/(\d+)/save_peer_review$', peer_review.save_peer_review),
    url(r'^course/(\d+)/peer_review/(\d+)/delete_peer_review$', peer_review.delete_peer_review),
    url(r'^course/(\d+)/peer_review/(\d+)/update_assignment_marks$', peer_review.update_assignment_marks),
                       
    # Discussion
    url(r'^course/(\d+)/discussion$', discussion.discussion_page),
    url(r'^course/(\d+)/threads_table$', discussion.threads_table),
    url(r'^course/(\d+)/new_thread$', discussion.new_thread_modal),
    url(r'^course/(\d+)/insert_thread$', discussion.insert_thread),
    url(r'^course/(\d+)/delete_thread$', discussion.delete_thread),                   
    url(r'^course/(\d+)/thread/(\d+)$', discussion.thread_page),
    url(r'^course/(\d+)/thread/(\d+)/posts_table$', discussion.posts_table),
    url(r'^course/(\d+)/thread/(\d+)/new_post$', discussion.new_post_modal),
    url(r'^course/(\d+)/thread/(\d+)/insert_post$', discussion.insert_post),
                       
    # Credit
    url(r'^course/(\d+)/credit$', credit.credit_page),
    url(r'^course/(\d+)/submit_credit_application$', credit.submit_credit_application),
)
