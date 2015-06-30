from django.conf.urls import patterns, include, url

from landpage.views import txt
from landpage.views import landpage
from landpage.views import privacy
from landpage.views import terms
from landpage.views import forgot_password
from landpage.views import google

urlpatterns = patterns('',
    # Custom Files
    url(r'^robots\.txt$', txt.robots_txt_page),
    url(r'^humans\.txt$', txt.humans_txt_page),
                       
    # Google Verify
    url(r'^googlee81f1c16590924d1.html$', google.google_verify_page),
    url(r'^googlee81f1c16590924d1$', google.google_verify_page),
                       
    # Landpage
    url(r'^$', landpage.landpage_page),
    url(r'^landpage$', landpage.landpage_page),
    url(r'^course_preview_modal$', landpage.course_preview_modal),
    url(r'^save_contact_us_message$', landpage.save_contact_us_message),
                       
    # Off-Convas Stuff
    url(r'^terms$', terms.terms_page),
    url(r'^privacy', privacy.privacy_page),
    url(r'^forgot_password$', forgot_password.forgot_password_page),
    url(r'^reset_password$', forgot_password.reset_password),
)

# Captchas
urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)