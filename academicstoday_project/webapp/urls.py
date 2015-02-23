from django.conf.urls import patterns, include, url

from . import views

# Import custom views.
from webapp.views import landpage
from webapp.views import courses
from webapp.views import course
from webapp.views import course
from webapp.views import file
urlpatterns = patterns('',
    # Custom Files
    url(r'^robots\.txt$', file.load_robots_txt),
    url(r'^humans\.txt$', file.load_humans_txt),
            
    # Landpage
    url(r'^$', landpage.load_landpage),
    url(r'^landpage$', landpage.load_landpage),
    url(r'^get_course_preview$', landpage.get_course_preview),
    url(r'^get_login$', landpage.get_login),
    url(r'^get_register$', landpage.get_register),
    url(r'^register$', landpage.register),
    url(r'^login$', landpage.login_authentication),
    url(r'^logout$', landpage.logout_authentication),
  
    # Course(s) & Enrolment
    url(r'^courses$', courses.courses),
    url(r'^enroll$', courses.enroll),
   
    # Course
    url(r'^course/(\d)/$', course.course),
    url(r'^course/(\d)/home$', course.course_home),
    url(r'^course/(\d)/syllabus$', course.course_syllabus),
    url(r'^course/(\d)/policy$', course.course_policy),
    url(r'^course/(\d)/lectures$', course.course_lectures),
    url(r'^course/(\d)/assignments$', course.course_assignments),
    url(r'^course/(\d)/quizzes$', course.course_quizzes),
    url(r'^course/(\d)/exams$', course.course_exams),
    url(r'^course/(\d)/discussion$', course.course_discussion),
    url(r'^course/(\d)/get_lecture$', course.get_lecture),
)