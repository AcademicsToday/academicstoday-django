from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    # Custom Files
    url(r'^robots\.txt$', views.robots_txt_page),
    url(r'^humans\.txt$', views.humans_txt_page),
                       
    # Landpage
    url(r'^$', views.landpage_page),
    url(r'^landpage$', views.landpage_page),
    url(r'^course_preview_modal$', views.course_preview_modal),
    url(r'^login_modal$', views.login_modal),
    url(r'^register_modal$', views.register_modal),
    url(r'^terms\.txt$', views.terms_txt_page),
    url(r'^privacy\.txt$', views.privacy_txt_page),
    url(r'^save_contact_us_message$', views.save_contact_us_message),
)