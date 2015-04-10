from django.conf.urls import patterns, include, url
from publisher.views import catalog

urlpatterns = patterns('',
    # Certificate(s)
    url(r'^publish$', catalog.catalog_page),
#    url(r'^certificates_table$', certificate.certificates_table),
#    url(r'^change_certificate_accessiblity$', certificate.change_certificate_accessiblity),
#    url(r'^certificate/(\d+)$', certificate.certificate_page),
#    url(r'^certificate_permalink_modal$', certificate.certificate_permalink_modal),
)
