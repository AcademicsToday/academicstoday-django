from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from shared_dashboard.views import web_views


urlpatterns = (
    url(r'^dashboard$', web_views.master_page, name='at_dashboard_master'),
)
