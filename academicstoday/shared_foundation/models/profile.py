# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_tenants.models import TenantMixin, DomainMixin
from shared_foundation import constants
from shared_foundation.utils import generate_hash


def get_expiry_date(days=2):
    """Returns the current date plus paramter number of days."""
    return timezone.now() + timedelta(days=days)


class SharedProfileManager(models.Manager):
    def delete_all(self):
        items = SharedProfile.objects.all()
        for item in items.all():
            item.delete()

    def get_by_email_or_none(self, email):
        try:
            return self.get(user__email=email)
        except SharedProfile.DoesNotExist:
            return None

    def get_by_user_or_none(self, user):
        try:
            return self.get(user=user)
        except SharedProfile.DoesNotExist:
            return None


class SharedProfile(models.Model):
    class Meta:
        app_label = 'shared_foundation'
        db_table = 'at_shared_profiles'
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    objects = SharedProfileManager()

    #
    #  FIELDS
    #

    user = models.OneToOneField(
        User,
        help_text=_('The user whom belongs to this profile.'),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        db_index=True,
    )

    #
    #  SYSTEM FIELDS
    #

    created = models.DateTimeField(auto_now_add=True, db_index=True,)
    last_modified = models.DateTimeField(auto_now=True, db_index=True,)
    salt = models.CharField( #DEVELOPERS NOTE: Used for cryptographic signatures.
        _("Salt"),
        max_length=127,
        help_text=_('The unique salt value associated with this object.'),
        default=generate_hash,
        unique=True,
        blank=True,
        null=True
    )

    #
    # PASSWORD RESET FIELDS
    #

    pr_access_code = models.CharField(
        _("Password Reset Access Code"),
        max_length=127,
        help_text=_('The access code to enter the password reset page to be granted access to restart your password.'),
        blank=True,
        default=generate_hash,
    )
    pr_expiry_date = models.DateTimeField(
        _('Password Reset Access Code Expiry Date'),
        help_text=_('The date where the access code expires and no longer works.'),
        blank=True,
        default=get_expiry_date,
    )

    #
    #  FUNCTIONS
    #

    def __str__(self):
        return str(self.name)

    def generate_pr_code(self):
        """
        Function generates a new password reset code and expiry date.
        """
        self.pr_access_code = generate_hash()
        self.pr_expiry_date = get_expiry_date()
        self.save()
        return self.pr_access_code

    def has_pr_code_expired(self):
        """
        Returns true or false depending on whether the password reset code
        has expired or not.
        """
        today = timezone.now()
        return today >= self.pr_expiry_date
