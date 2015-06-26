from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^login_modal$', views.login_modal),
    url(r'^login$', views.login_authentication),
    url(r'^logout$', views.logout_authentication),

)