from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_tenants.models import TenantMixin, DomainMixin
from shared_foundation import constants
from shared_foundation.models.abstract_bigpk import AbstractSharedBigPk
from shared_foundation.models.abstract_thing import AbstractSharedThing


class SharedUniversityRegistration(AbstractSharedBigPk, AbstractSharedThing):
    class Meta:
        app_label = 'shared_foundation'
        db_table = 'at_shared_univeristy_registrations'
        verbose_name = _('University Registration')
        verbose_name_plural = _('University Registrations')

    schema_name = models.CharField(
        _("Legal Name"),
        max_length=255,
        help_text=_('The official name of the organization, e.g. the registered company name.'),
        blank=True,
        null=True,
    )
    name = models.CharField(
        _("Legal Name"),
        max_length=255,
        help_text=_('The official name of the organization, e.g. the registered company name.'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.name)
