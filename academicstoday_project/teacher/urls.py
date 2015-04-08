from django.conf.urls import patterns, include, url

from . import views

# Import custom views.
from teacher.views import announcement
from teacher.views import syllabus
from teacher.views import policy
from teacher.views import lecture
from teacher.views import lecture_note
from teacher.views import assignment
from teacher.views import quiz
from teacher.views import exam
from teacher.views import overview
from teacher.views import discussion
from teacher.views import peer_review
from teacher.views import setting

urlpatterns = patterns('',
    # Syllabus
    url(r'^teacher/course/(\d+)/overview$', overview.overview_page),
    url(r'^teacher/course/(\d+)/submit_course_for_review$', overview.submit_course_for_review),

    # Announcement
    url(r'^teacher/course/(\d+)/$', announcement.announcements_page),
    url(r'^teacher/course/(\d+)/home$', announcement.announcements_page),
    url(r'^teacher/course/(\d+)/announcement$', announcement.announcements_page),
    url(r'^teacher/course/(\d+)/announcements_table$', announcement.announcements_table),
    url(r'^teacher/course/(\d+)/announcement_modal$', announcement.announcement_modal),
    url(r'^teacher/course/(\d+)/save_announcement$', announcement.save_announcement),
    url(r'^teacher/course/(\d+)/delete_announcement$', announcement.delete_announcement),

    # Syllabus
    url(r'^teacher/course/(\d+)/syllabus$', syllabus.syllabus_page),
    url(r'^teacher/course/(\d+)/syllabus_modal$', syllabus.syllabus_modal),
    url(r'^teacher/course/(\d+)/save_syllabus$', syllabus.save_syllabus),
    url(r'^teacher/course/(\d+)/delete_syllabus$', syllabus.delete_syllabus),

    # Policy
    url(r'^teacher/course/(\d+)/policy$', policy.policy_page),
    url(r'^teacher/course/(\d+)/policy_modal$', policy.policy_modal),
    url(r'^teacher/course/(\d+)/save_policy$', policy.save_policy),
    url(r'^teacher/course/(\d+)/delete_policy$', policy.delete_policy),

    # Lecture
    url(r'^teacher/course/(\d+)/lectures$', lecture.lectures_page),
    url(r'^teacher/course/(\d+)/lectures_table$', lecture.lectures_table),
    url(r'^teacher/course/(\d+)/lecture_modal$', lecture.lecture_modal),
    url(r'^teacher/course/(\d+)/save_lecture$', lecture.save_lecture),
    url(r'^teacher/course/(\d+)/delete_lecture$', lecture.delete_lecture),

    # Lecture Note(s)
    url(r'^teacher/course/(\d+)/lecture/(\d+)/notes$', lecture_note.lecture_notes_page),
    url(r'^teacher/course/(\d+)/lecture/(\d+)/lecture_notes_table$', lecture_note.lecture_notes_table),
    url(r'^teacher/course/(\d+)/lecture/(\d+)/lecture_note_modal$', lecture_note.lecture_note_modal),
    url(r'^teacher/course/(\d+)/lecture/(\d+)/save_lecture_note$', lecture_note.save_lecture_note),
    url(r'^teacher/course/(\d+)/lecture/(\d+)/delete_lecture_note$', lecture_note.delete_lecture_note),
                       
    # Assignment(s)
    url(r'^teacher/course/(\d+)/assignments$', assignment.assignments_page),
    url(r'^teacher/course/(\d+)/assignments_table$', assignment.assignments_table),
    url(r'^teacher/course/(\d+)/assignment_modal$', assignment.assignment_modal),
    url(r'^teacher/course/(\d+)/save_assignment$', assignment.save_assignment),
    url(r'^teacher/course/(\d+)/delete_assignment$', assignment.delete_assignment),

    # Assignment
    url(r'^teacher/course/(\d+)/assignment/(\d+)$', assignment.assignment_page),
    url(r'^teacher/course/(\d+)/assignment/(\d+)/questions_table$', assignment.questions_table),
    url(r'^teacher/course/(\d+)/assignment/(\d+)/question_type_modal$', assignment.question_type_modal),
    url(r'^teacher/course/(\d+)/assignment/(\d+)/question_essay_modal$', assignment.question_essay_modal),
    url(r'^teacher/course/(\d+)/assignment/(\d+)/question_multiple_choice_modal$', assignment.question_multiple_choice_modal),
    url(r'^teacher/course/(\d+)/assignment/(\d+)/question_true_false_modal$', assignment.question_true_false_modal),
    url(r'^teacher/course/(\d+)/assignment/(\d+)/question_response_modal$', assignment.question_response_modal),
    url(r'^teacher/course/(\d+)/assignment/(\d+)/save_question$', assignment.save_question),
    url(r'^teacher/course/(\d+)/assignment/(\d+)/delete_question$', assignment.delete_question),

    # Quiz(es)
    url(r'^teacher/course/(\d+)/quizzes$', quiz.quizzes_page),
    url(r'^teacher/course/(\d+)/quizzes_table$', quiz.quizzes_table),
    url(r'^teacher/course/(\d+)/quiz_modal$', quiz.quiz_modal),
    url(r'^teacher/course/(\d+)/save_quiz$', quiz.save_quiz),
    url(r'^teacher/course/(\d+)/delete_quiz$', quiz.delete_quiz),

    # Quiz
    url(r'^teacher/course/(\d+)/quiz/(\d+)$', quiz.quiz_page),
    url(r'^teacher/course/(\d+)/quiz/(\d+)/questions_table$', quiz.questions_table),
    url(r'^teacher/course/(\d+)/quiz/(\d+)/question_type_modal$', quiz.question_type_modal),
    url(r'^teacher/course/(\d+)/quiz/(\d+)/question_true_false_modal$', quiz.question_true_false_modal),
    url(r'^teacher/course/(\d+)/quiz/(\d+)/save_question$', quiz.save_question),
    url(r'^teacher/course/(\d+)/quiz/(\d+)/delete_question$', quiz.delete_question),

    # Exam(s)
    url(r'^teacher/course/(\d+)/exams$', exam.exams_page),
    url(r'^teacher/course/(\d+)/exams_table$', exam.exams_table),
    url(r'^teacher/course/(\d+)/exam_modal$', exam.exam_modal),
    url(r'^teacher/course/(\d+)/save_exam$', exam.save_exam),
    url(r'^teacher/course/(\d+)/delete_exam$', exam.delete_exam),
    
    # # Exam
    url(r'^teacher/course/(\d+)/exam/(\d+)$', exam.exam_page),
    url(r'^teacher/course/(\d+)/exam/(\d+)/questions_table$', exam.questions_table),
    url(r'^teacher/course/(\d+)/exam/(\d+)/question_type_modal$', exam.question_type_modal),
    url(r'^teacher/course/(\d+)/exam/(\d+)/question_multiple_choice_modal$', exam.question_multiple_choice_modal),
    url(r'^teacher/course/(\d+)/exam/(\d+)/save_question$', exam.save_question),
    url(r'^teacher/course/(\d+)/exam/(\d+)/delete_question$', exam.delete_question),
                       
    # Discussion
    url(r'^teacher/course/(\d+)/discussion$', discussion.discussion_page),
    url(r'^teacher/course/(\d+)/discussions_table$', discussion.discussions_table),
    url(r'^teacher/course/(\d+)/new_thread$', discussion.new_thread_modal),
    url(r'^teacher/course/(\d+)/insert_thread$', discussion.insert_thread),
    url(r'^teacher/course/(\d+)/delete_thread$', discussion.delete_thread),
    url(r'^teacher/course/(\d+)/thread/(\d+)$', discussion.posts_page),
    url(r'^teacher/course/(\d+)/thread/(\d+)/posts_table$', discussion.posts_table),
    url(r'^teacher/course/(\d+)/thread/(\d+)/new_post$', discussion.new_post_modal),
    url(r'^teacher/course/(\d+)/thread/(\d+)/insert_post$', discussion.insert_post),
                       
    # Peer-Review
    url(r'^teacher/course/(\d+)/peer_reviews$', peer_review.peer_reviews_page),
    url(r'^teacher/course/(\d+)/peer_review/(\d+)$', peer_review.assignment_page),
    url(r'^teacher/course/(\d+)/peer_review/(\d+)/peer_review_modal$', peer_review.peer_review_modal),
    url(r'^teacher/course/(\d+)/peer_review/(\d+)/save_peer_review$', peer_review.save_peer_review),
    url(r'^teacher/course/(\d+)/peer_review/(\d+)/delete_peer_review$', peer_review.delete_peer_review),
    url(r'^teacher/course/(\d+)/peer_review/(\d+)/update_assignment_marks$', peer_review.update_assignment_marks),
                       
    # Settings
    url(r'^teacher/course/(\d+)/settings$', setting.settings_page),
    url(r'^teacher/course/(\d+)/suspend_course$', setting.suspend_course),
)
