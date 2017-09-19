# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from shared_foundation import utils
from shared_foundation import constants
from shared_foundation import models


def user_activation_email_page(request, pr_access_code=""):
    """
    Email web-view of the welcome customer.
    """
    url = utils.reverse_with_full_domain(
        reverse_url_id='at_register_user_activation_detail',
        resolve_url_args=[pr_access_code]
    )
    web_view_extra_url = utils.reverse_with_full_domain(
        reverse_url_id='at_register_user_activation_email_master',
        resolve_url_args=[pr_access_code]
    )
    return render(request, 'shared_authentication/email/user_activation_email_view.html',{
        'url': url,
        'web_view_extra_url': web_view_extra_url
    })
