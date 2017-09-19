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
    help = 'Command will send an email to the user that their university has been created.'

    def add_arguments(self, parser):
        parser.add_argument('email', nargs='+', type=str)
        parser.add_argument('schema_name', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            email = options['email'][0]
            schema_name = options['schema_name'][0]
            user = User.objects.get(email__iexact=email)
            university = models.SharedUniversity.objects.get(schema_name=schema_name)
            self.begin_processing(user, university)
        except User.DoesNotExist:
            raise CommandError(_('AT: User does not exist with the email: %s') % str(email))
        except models.SharedUniversity.DoesNotExist:
            raise CommandError(_('AT: User does not exist with the email: %s') % str(email))

    def begin_processing(self, user, university):
        subject = "Acdemics Today: University Founded!"
        param = {
            'user': user,
            'university': university
        }

        # Plug-in the data into our templates and render the data.
        text_content = render_to_string('shared_university/email/unversity_founded_email.txt', param)
        html_content = render_to_string('shared_university/email/unversity_founded_email.html', param)

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
