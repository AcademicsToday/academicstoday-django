from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^login$', views.login_authentication),
    url(r'^logout$', views.logout_authentication),

)