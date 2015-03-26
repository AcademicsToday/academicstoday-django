from django.conf.urls import patterns, include, url

from . import views
from account.views import login
from account.views import mail
from account.views import profile
from account.views import registration
from account.views import setting

urlpatterns = patterns('',
    url(r'^register$', registration.register),
    url(r'^login$', login.login_authentication),
    url(r'^logout$', login.logout_authentication),
    url(r'^profile$', profile.profile_page),
    url(r'^inbox$', mail.inbox_page),
    url(r'^settings$', setting.settings_page),
)