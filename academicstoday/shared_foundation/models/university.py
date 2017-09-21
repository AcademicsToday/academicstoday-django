from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_tenants.models import TenantMixin, DomainMixin
from shared_foundation.models.abstract_thing import AbstractSharedThing
from shared_foundation import constants


class SharedUniversity(TenantMixin, AbstractSharedThing):
    class Meta:
        app_label = 'shared_foundation'
        db_table = 'at_shared_universities'
        verbose_name = _('University')
        verbose_name_plural = _('Universities')

    #
    #  SYSTEM FIELDS
    #

    created = models.DateTimeField(auto_now_add=True, db_index=True,)
    last_modified = models.DateTimeField(auto_now=True, db_index=True,)

    #
    # GENERIC FIELDS
    #

    administrators = models.ManyToManyField(
        User,
        help_text=_('The users who are office staff and administrators of this university.'),
        blank=True,
        related_name="%(app_label)s_%(class)s_staff_related"
    )
    teachers = models.ManyToManyField(
        User,
        help_text=_('The users who are teachers in this university.'),
        blank=True,
        related_name="%(app_label)s_%(class)s_teachers_related"
    )
    students = models.ManyToManyField(
        User,
        help_text=_('The users who are students in this university.'),
        blank=True,
        related_name="%(app_label)s_%(class)s_students_related"
    )
    applicants = models.ManyToManyField(
        User,
        help_text=_('The users who have applied to this university and require admission decision by an administrator.'),
        blank=True,
        related_name="%(app_label)s_%(class)s_applicants_related"
    )
    is_listed = models.BooleanField(
        _("Is Listed"),
        help_text=_('Variable controls whether this university will be listed to the public.'),
        default=True,
        blank=True
    )
    is_content_open = models.BooleanField(
        _("Is Content Open"),
        help_text=_('Variable controls whether non-registered users are able to view the contents of the university or users must be registered to view. This includes: courses, forums, etc.'),
        default=True,
        blank=True
    )
    registration_requirement = models.PositiveSmallIntegerField(
        _("Registration Reqirement"),
        choices=constants.REGISTRATION_REQUIREMENT_OPTIONS,
        help_text=_('The registration requirement for students to be accepted into this university.'),
        default=constants.NO_REGISTRATION_REQUIREMENT_ID,
        blank=True
    )

    def __str__(self):
        return str(self.name)

    def is_member(self, user):
        """
        Function returns TRUE/FALSE depending on whether the user somehow
        belongs to this university or not.
        """
        if user in self.administrators.all():
            return True
        elif user in self.teachers.all():
            return True
        elif user in self.students.all():
            return True
        else:
            return False

    def is_applicant(self, user):
        """
        Functions returns TRUE/FALSE depending if user is an applicant in
        this university.
        """
        if user in self.applicants.all():
            return True
        else:
            return False


class SharedUniveristyDomain(DomainMixin):
    class Meta:
        app_label = 'shared_foundation'
        db_table = 'at_shared_domains'
        verbose_name = _('Domain')
        verbose_name_plural = _('Domains')

    pass
