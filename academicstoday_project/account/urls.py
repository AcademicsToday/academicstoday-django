from django.conf.urls import patterns, include, url
from account.views import mail
from account.views import profile
from account.views import setting
from account.views import donate

urlpatterns = patterns('',
    url(r'^profile$', profile.profile_page),
    url(r'^update_user$', profile.update_user),
    url(r'^inbox$', mail.mail_page),
    url(r'^send_private_message$', mail.send_private_message),
    url(r'^view_private_message$', mail.view_private_message),
    url(r'^delete_private_message$', mail.delete_private_message),
    url(r'^settings$', setting.settings_page),
    url(r'^update_password$', setting.update_password),
    url(r'^donate$', donate.donate_page),
)