from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from shared_index import views


urlpatterns = (
    url(r'^$', views.index_page, name='at_index_master'),
    url(r'^en$', views.index_page),
    url(r'^en/$', views.index_page),
    # url(r'^sample/push_notification$', views.sample_page, name='sample_view_master'),
    # url(r'^error/no-storage$', views.no_storage_supported_page, name='at_no_storage_supported_master'),
)
