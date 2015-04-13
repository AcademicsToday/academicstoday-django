from django.conf.urls import patterns, include, url

from registrar.views import courses
from registrar.views import enrolment
from registrar.views import teaching
from registrar.views import transcript
from registrar.views import certificate

urlpatterns = patterns('',
    # Courses
    url(r'^courses$', courses.courses_page),
    url(r'^enrol$', courses.enrol),

    # Enrolment(s)
    url(r'^enrolment$', enrolment.enrolment_page),
    url(r'^enrolment_table$', enrolment.enrolment_table),
    url(r'^disenroll_modal$', enrolment.disenroll_modal),
    url(r'^disenrol', enrolment.disenrol),
         
    # Teaching
    url(r'^teaching$', teaching.teaching_page),
    url(r'^refresh_teaching_table$', teaching.refresh_teaching_table),
                       
    url(r'^course_modal$', teaching.course_modal),
    url(r'^save_course$', teaching.save_course),
    url(r'^delete_course_modal$', teaching.delete_course_modal),
    url(r'^course_delete$', teaching.course_delete),
                    
    # Transcript
    url(r'^transcript$', transcript.transcript_page),
                       
    # Certificate(s)
    url(r'^certificates$', certificate.certificates_page),
    url(r'^certificates_table$', certificate.certificates_table),
    url(r'^change_certificate_accessiblity$', certificate.change_certificate_accessiblity),
    url(r'^certificate/(\d+)$', certificate.certificate_page),
    url(r'^certificate_permalink_modal$', certificate.certificate_permalink_modal),
)
