from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    # Courses
    url(r'^courses$', views.courses_page),
    url(r'^enrol$', views.enrol),

    # Enrolment(s)
    url(r'^enrolment$', views.enrolment_page),
                       
    # Teaching
    url(r'^teaching$', views.teaching_page),
    url(r'^new_course_modal$', views.new_course_modal),
    url(r'^save_new_course$', views.save_new_course),
    url(r'^course_delete$', views.course_delete),
                    
    # Transcript
    url(r'^transcript$', views.transcript_page),
                       
    # Certificate(s)
    url(r'^certificates$', views.certificates_page),
)
