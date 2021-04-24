from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^register_modal$', views.register_modal),
    url(r'^register$', views.register),
]