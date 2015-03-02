from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    # Course(s) & Enrolment
    url(r'^courses$', views.courses),
    url(r'^enroll$', views.enroll),
)