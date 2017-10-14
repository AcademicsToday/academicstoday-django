from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from shared_course.views import web_views


urlpatterns = (
    url(r'^courses$', web_views.master_page, name='at_course_master'),
    url(r'^course/(.*)/$', web_views.detail_page, name='at_course_detail'),
)
