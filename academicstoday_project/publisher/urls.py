from django.conf.urls import patterns, include, url
from publisher.views import catalog
from publisher.views import my_publication
from publisher.views import publication

urlpatterns = patterns('',
    # Publications(s)
    url(r'^publish$', catalog.catalog_page),
    url(r'^publication/(\d+)$', publication.publication_page),
    url(r'^publication/(\d+)/peer_review_modal$', publication.peer_review_modal),
    url(r'^publication/(\d+)/save_peer_review$', publication.save_peer_review),
    url(r'^publication/(\d+)/delete_peer_review$', publication.delete_peer_review),
                       
    # My Publications
    url(r'^my_publications$', my_publication.my_publications_page),
    url(r'^refresh_publications_table$', my_publication.refresh_publications_table),
    url(r'^my_publication_modal$', my_publication.my_publication_modal),
    url(r'^save_publication$', my_publication.save_publication),
    url(r'^delete_publication$', my_publication.delete_publication),
)
