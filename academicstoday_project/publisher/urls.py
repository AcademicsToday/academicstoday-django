from django.conf.urls import patterns, include, url
from publisher.views import catalog
from publisher.views import my_publication

urlpatterns = patterns('',
    # Publications(s)
    url(r'^publish$', catalog.catalog_page),
                       
    # My Publications
    url(r'^my_publications$', my_publication.my_publications_page),
#    url(r'^change_certificate_accessiblity$', certificate.change_certificate_accessiblity),
#    url(r'^certificate/(\d+)$', certificate.certificate_page),
#    url(r'^certificate_permalink_modal$', certificate.certificate_permalink_modal),
)
