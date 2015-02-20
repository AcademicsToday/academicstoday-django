from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    # Search Engine
    url(r'^robots\.txt$', landpage.load_robots_txt),
    url(r'^humans\.txt$', landpage.load_humans_txt),
            
    # Landpage
    url(r'^$', views.load_landpage),
    url(r'^landpage$', views.load_landpage),
    url(r'^get_course_preview$', views.get_course_preview),
    url(r'^get_login$', views.get_login),
    url(r'^get_register$', views.get_register),
    url(r'^register$', views.register),
    url(r'^login$', views.login_authentication),
    url(r'^logout$', views.logout_authentication),
  
    # Course(s) & Enrolment
    url(r'^courses$', views.courses),
    url(r'^enroll$', views.enroll),
   
    # Course
    url(r'^course/(\d)/$', views.course),
    url(r'^course/(\d)/home$', views.course_home),
    url(r'^course/(\d)/syllabus$', views.course_syllabus),
    url(r'^course/(\d)/policy$', views.course_policy),
    url(r'^course/(\d)/lectures$', views.course_lectures),
    url(r'^course/(\d)/assignments$', views.course_assignments),
    url(r'^course/(\d)/quizzes$', views.course_quizzes),
    url(r'^course/(\d)/exams$', views.course_exams),
    url(r'^course/(\d)/discussion$', views.course_discussion),
)