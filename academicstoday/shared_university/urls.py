from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from shared_university.views import web_views


urlpatterns = (
    url(r'^university/founding$', web_views.create_master_page, name='at_university_founding_master'),
    url(r'^university/founding/completed$', web_views.create_detail_page, name='at_university_founding_detail'),

)
