from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives    # EMAILER
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string    # HTML to TXT
from django.utils.translation import ugettext_lazy as _
from shared_foundation import constants
from shared_foundation import models
from shared_foundation import utils


class Command(BaseCommand):
    help = 'Command will send an activation email to a university admin user.'

    def add_arguments(self, parser):
        parser.add_argument('email', nargs='+')

    def handle(self, *args, **options):
        """
        Function will send an email to the existing User account (in our system)
        for the inputted "email" and will attach in the message the link which
        once clicked on by the User will cause the account's password to be
        reset.
        """
        try:
            for email in options['email']:
                user = User.objects.get(email__iexact=email)
                self.begin_processing(user)

        except User.DoesNotExist:
            raise CommandError(_('AT: User does not exist with the email: %s') % str(email))

    def begin_processing(self, user):
        pr_access_code = None

        profile = models.SharedProfile.objects.get_by_user_or_none(user)
        if profile:
            pr_access_code = profile.generate_pr_code()
            if pr_access_code == None:
                raise CommandError(_('No pr_access_code text found for this Customer!'))
        else:
            raise CommandError(_('No profile object found!'))

        url = utils.reverse_with_full_domain(
            reverse_url_id='at_register_user_activation_detail',
            resolve_url_args=[pr_access_code]
        )
        web_view_extra_url = utils.reverse_with_full_domain(
            reverse_url_id='at_register_user_activation_email_master',
            resolve_url_args=[pr_access_code]
        )
        subject = "Acdemics Today: Activation"
        param = {
            'url': url,
            'web_view_extra_url': web_view_extra_url
        }

        # Plug-in the data into our templates and render the data.
        text_content = render_to_string('shared_authentication/email/user_activation_email_view.txt', param)
        html_content = render_to_string('shared_authentication/email/user_activation_email_view.html', param)

        # Generate our address.
        from_email = settings.DEFAULT_FROM_EMAIL
        to = [user.email]

        # Send the email.
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        self.stdout.write(
            self.style.SUCCESS(_('Successfully sent welcome email to %s.') % str(user.email))
        )
