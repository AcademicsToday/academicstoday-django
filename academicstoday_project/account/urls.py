from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    # Custom Files
    url(r'^register$', views.register),
    url(r'^login$', views.login_authentication),
    url(r'^logout$', views.logout_authentication),
)