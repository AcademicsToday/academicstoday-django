from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import serializers, viewsets, routers
from rest_framework.urlpatterns import format_suffix_patterns
from shared_api.views.obtainauthtoken_view import ObtainAuthTokenAPIView
from shared_api.views.register_user_view import RegisterUserAPIView
from shared_api.views.register_university_view import RegisterUniversityAPIView


urlpatterns = [
    # Authentication.
    url(r'^api/get_token$', ObtainAuthTokenAPIView.as_view()),
    url(r'^api/register/user/$', RegisterUserAPIView.as_view()),

    # University
    url(r'^api/register/university/$', RegisterUniversityAPIView.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)
