from django.conf.urls import patterns, include, url

from landpage.views import txt
from landpage.views import landpage
from landpage.views import login
from landpage.views import register

urlpatterns = patterns('',
    # Custom Files
    url(r'^robots\.txt$', txt.robots_txt_page),
    url(r'^humans\.txt$', txt.humans_txt_page),
    url(r'^terms\.txt$', txt.terms_txt_page),
    url(r'^privacy\.txt$', txt.privacy_txt_page),
                       
    # Landpage
    url(r'^$', landpage.landpage_page),
    url(r'^landpage$', landpage.landpage_page),
    url(r'^course_preview_modal$', landpage.course_preview_modal),
    url(r'^save_contact_us_message$', landpage.save_contact_us_message),

    # Login
    url(r'^login_modal$', login.login_modal),

    # Regsiter
    url(r'^register_modal$', register.register_modal),
)

# Captchas
urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)