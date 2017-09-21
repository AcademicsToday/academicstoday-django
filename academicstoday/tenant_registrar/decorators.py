from functools import wraps
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import resolve, reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from shared_foundation import constants


def tenant_registration_required(view_func):
    """
    Decorater checks to see if accessing the view requires registration for
    the university. If registration is required then the user will be redirected
    to the registrar page. If the user is locked out or the registration has
    been locked down then the proper redirection will occur.
    """
    def process_open_registration(request):
        """
        Check to see if the user is a student if not then redirect to a
        registration page for the user to fill out.
        """
        if not request.tenant.is_applicant(request.user):
            return HttpResponseRedirect(reverse('at_tenant_registrar_master'))
        else:
            return HttpResponseRedirect(reverse('at_tenant_registrar_detail'))

    def process_restrictive_registration(request):
        print("TODO: Restrictive Registration Required")

    def process_closed_registration(request):
        return HttpResponseRedirect(reverse('at_tenant_registrar_closed'))

    def wrapper(request, *args, **kwargs):
        if request.user is not None:
            if request.user.is_authenticated():
                if request.tenant:
                    if not request.tenant.is_member(request.user):
                        if request.tenant.registration_requirement == constants.NO_REGISTRATION_REQUIREMENT_ID:
                            pass

                        elif request.tenant.registration_requirement == constants.OPEN_REGISTRATION_REQUIREMENT_ID:
                            return process_open_registration(request)

                        elif request.tenant.registration_requirement == constants.RESTRICTIVE_REGISTRATION_REQUIREMENT_ID:
                            return process_restrictive_registration(request)

                        elif request.tenant.registration_requirement == constants.CLOSED_REGISTRATION_REQUIREMENT_ID:
                            return process_closed_registration(request)

        return view_func(request, *args, **kwargs)
    return wrapper
