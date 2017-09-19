# -*- coding: utf-8 -*-
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework.authtoken.models import Token
from foundation_app import constants


class AcademicsTodayTokenMiddleware(object):
    """
        The purpose of this middleware is to attach a 'token' variable to
        the request if the User has been logged in and if a Token does not
        exist then create one.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated():
            try:
                request.token = Token.objects.get(user_id=request.user.id)
            except Token.DoesNotExist:
                request.token = Token.objects.create(user_id=request.user.id)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        # (Do Nothing ...)

        return response  # Finish our middleware handler.


class AcademicsTodayIPAddressMiddleware(object):
    """
        Utility middleware for getting the IP. Source: http://stackoverflow.com/a/4581997
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Discover the IP address of the user and attach it to the request.
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            request.ip_address = x_forwarded_for.split(',')[0]
        else:
            request.ip_address = request.META.get('REMOTE_ADDR')

        # Run the view.
        return self.get_response(request)
