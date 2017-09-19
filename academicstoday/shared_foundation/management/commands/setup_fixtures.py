import os
import sys
from decimal import *
from django.db.models import Sum
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from django.core.management import call_command


class Command(BaseCommand):
    help = _('Loads all the data necessary to operate this application.')

    def handle(self, *args, **options):
        # The filename of all the objects to be imported.
        ordered_file_names = [
            'sites.json',
        ]

        # Iterate through all the filenames and load them into database.
        for file_name in ordered_file_names:
            call_command('loaddata', file_name, verbosity=0, interactive=False)

        self.stdout.write(
            self.style.SUCCESS(_('Successfully imported fixtures'))
        )


#-----------------
# DEVELOPER NOTES:
#-----------------
# Loading
#-----------
# Remember, if you want to load up a fixture from console, run:
# python manage.py loaddata all.json
#
# Exporting
#------------
# To export data to a fixture, use the following code examples.
#
# Export entire application:
# python manage.py dumpdata --indent 4 --format=json > ~/Desktop/all.json
#
# Export all the data inside an application:
# python manage.py dumpdata --indent 4 --format=json api > ~/Desktop/api.json
#
# Export specific data from an application:
# python manage.py dumpdata --indent 4 --format=json api.BannedDomain > ~/Desktop/banned_domains.json
#
# Export specific table from Django:
# python manage.py dumpdata --indent 4 --format=json auth.Group > ~/Desktop/groups.json
# python manage.py dumpdata --indent 4 --format=json auth.Permission > ~/Desktop/permissions.json
# python manage.py dumpdata --indent 4 --format=json auth.User > ~/Desktop/users.json
# python manage.py dumpdata --indent 4 --format=json sites.Site > ~/Desktop/sites.json
