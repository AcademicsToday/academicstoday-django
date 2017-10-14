from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import serializers, viewsets, routers
from rest_framework.urlpatterns import format_suffix_patterns
# from tenant_api.views.login_view import LoginAPIView
# from tenant_api.views.logout_view import LogoutAPIView
# from tenant_api.views.obtainauthtoken_view import ObtainAuthTokenAPIView # DEPRECATED
# from tenant_api.views.register_user_view import RegisterUserAPIView
# from tenant_api.views.register_university_view import RegisterUniversityAPIView


urlpatterns = [
    # Authentication.
    # url(r'^api/login$', LoginAPIView.as_view()),
    # url(r'^api/logout$', LogoutAPIView.as_view()),
    # url(r'^api/get_token$', ObtainAuthTokenAPIView.as_view()), # DEPRECATED
    # url(r'^api/register/user/$', RegisterUserAPIView.as_view()),
    #
    # # University
    # url(r'^api/register/university/$', RegisterUniversityAPIView.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)
