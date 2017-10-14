# -*- coding: utf-8 -*-
import datetime
from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from shared_foundation import constants
from shared_foundation.models import SharedUniversity


register = template.Library()


@register.simple_tag
def get_app_domain():
    """
    Returns the full URL to the domain. The output from this function gets
    generally appended with a path string.
    """
    url = settings.ACADEMICSTODAY_APP_HTTP_PROTOCOL
    url += settings.ACADEMICSTODAY_APP_HTTP_DOMAIN
    return url


@register.simple_tag
def tenant_url(schema_name, view_name):
    if schema_name:
        return settings.ACADEMICSTODAY_APP_HTTP_PROTOCOL + schema_name + '.%s' % settings.ACADEMICSTODAY_APP_HTTP_DOMAIN + reverse(view_name)
    else:
        return settings.ACADEMICSTODAY_APP_HTTP_PROTOCOL + '%s' % settings.ACADEMICSTODAY_APP_HTTP_DOMAIN + reverse(view_name)


@register.inclusion_tag('templatetags/render_shared_sidebar_menu.html')
def render_shared_sidebar_menu(page_id, user=None):
    """
    TODO
    """
    # Fetch all the univeristies in our system which are publicaly listed.
    my_universities = SharedUniversity.objects.filter(
        Q(administrators__id=user.id) |
        Q(teachers__id=user.id) |
        Q(students__id=user.id)
    ).prefetch_related(
        'administrators',
        'teachers',
        'students'
    )

    # Return our objects for this view.
    return {
        'page_id': page_id,
        'user': user,
        'my_universities': my_universities
    }


@register.inclusion_tag('templatetags/render_shared_top_menu.html')
def render_shared_top_menu(page_id, user=None):
    """
    TODO
    """
    return {
        'page_id': page_id
    }
