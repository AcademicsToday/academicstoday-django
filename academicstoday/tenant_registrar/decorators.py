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
    def wrapper(request, *args, **kwargs):
        if request.user is not None:
            if request.user.is_authenticated():
                if request.tenant:
                    print("TODO") #TODO: Add registation check + redirect code.
                    # return HttpResponseRedirect(reverse('tenant_intake_entr_round_one_step_one'))

        return view_func(request, *args, **kwargs)
    return wrapper
