from django.conf.urls import patterns, include, url

from . import views

# Import custom views.
from webapp.views import file
urlpatterns = patterns('',
    # Custom Files
    url(r'^robots\.txt$', file.load_robots_txt),
    url(r'^humans\.txt$', file.load_humans_txt),
            
    # Landpage
    url(r'^$', views.load_landpage),
    url(r'^landpage$', views.load_landpage),
    url(r'^get_course_preview$', views.get_course_preview),
    url(r'^get_login$', views.get_login),
    url(r'^get_register$', views.get_register),
)