# -*- coding: utf-8 -*-
import datetime
from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from shared_foundation import constants


register = template.Library()


@register.simple_tag
def university_gateway_url(university, user):
    """
    Function will lookup the user inside the university and generate a URL for
    the user to access the university. This function will generate the following
    urls:

    (1) University admin dashboard URL if the user is an administrator.
    (2) University student dashboard URL if the user is a student.
    (3) University teacher dashboard URL if the user is a teacher.
    (4) University registrar URL if the user is not a member.
    """
    if user in university.students.all():
        return settings.ACADEMICSTODAY_APP_HTTP_PROTOCOL + university.schema_name + '.%s' % settings.ACADEMICSTODAY_APP_HTTP_DOMAIN + reverse('at_tenant_student_dashboard_master')

    if user in university.teachers.all():
        return settings.ACADEMICSTODAY_APP_HTTP_PROTOCOL + university.schema_name + '.%s' % settings.ACADEMICSTODAY_APP_HTTP_DOMAIN + reverse('at_tenant_teacher_dashboard_master')

    if user in university.administrators.all():
        return settings.ACADEMICSTODAY_APP_HTTP_PROTOCOL + university.schema_name + '.%s' % settings.ACADEMICSTODAY_APP_HTTP_DOMAIN + reverse('at_tenant_admin_dashboard_master')

    return settings.ACADEMICSTODAY_APP_HTTP_PROTOCOL + university.schema_name + '.%s' % settings.ACADEMICSTODAY_APP_HTTP_DOMAIN + reverse('at_tenant_registrar_master')


@register.inclusion_tag('templatetags/tenant_foundation_tags.html')
def render_tenant_sidebar_menu(university, user):
    """
    TODO
    """
    return {
        'todo': None
    }
