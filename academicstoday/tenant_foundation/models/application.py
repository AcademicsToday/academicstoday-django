# -*- coding: utf-8 -*-
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from django.db.models import Q
from django.utils import timezone
from tenant_foundation import constants


class ApplicationManager(models.Manager):
    def delete_all(self):
        items = Application.objects.all()
        for item in items.all():
            item.delete()


class Application(models.Model):
    class Meta:
        app_label = 'tenant_foundation'
        db_table = 'at_applications'
        verbose_name = _('Application')
        verbose_name_plural = _('Applications')

    objects = ApplicationManager()
    user = models.ForeignKey(
        User,
        help_text=_('The user that this application belongs to.'),
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    status = models.PositiveSmallIntegerField(
        _("Status"),
        choices=constants.APPLICATION_STATUS_OPTIONS,
        help_text=_('The state of the application.'),
        default=constants.APPLICATION_CREATED_STATUS_ID,
        blank=True,
        db_index=True,
    )

    # DEVELOPERS NOTE:
    # These fields are used to track time/date of this application.
    created = models.DateTimeField(auto_now_add=True, db_index=True,)
    last_modified = models.DateTimeField(auto_now=True, db_index=True,)

    # This is used to track who was last
    last_modified_by = models.ForeignKey(
        User,
        help_text=_('The user whom last made changes to this object.'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_last_modified_by_related",
    )

    def __str__(self):
        return str(self.pk)
