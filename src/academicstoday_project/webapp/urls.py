from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.load_landpage),
    url(r'^get_course_preview$', views.get_course_preview),
    url(r'^get_login$', views.get_login),
    url(r'^get_register$', views.get_register),
)