from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    # Courses
    url(r'^courses$', views.courses_page),
    url(r'^enrol$', views.enrol),
           
    # My Courses
    url(r'^my_courses$', views.my_courses_page),
    url(r'^new_course_modal$', views.new_course_modal),
    url(r'^save_new_course$', views.save_new_course),                   
)