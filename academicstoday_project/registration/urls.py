from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^register_modal$', views.register_modal),
    url(r'^register$', views.register),
)