from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from tenant_registrar.views import web_views


urlpatterns = (
    url(r'^registrar/$', web_views.master_page, name='at_tenant_registrar_master'),
    url(r'^registrar/completed$', web_views.detail_page, name='at_tenant_registrar_detail'),
    url(r'^registrar/closed$', web_views.closed_page, name='at_tenant_registrar_closed'),

)
