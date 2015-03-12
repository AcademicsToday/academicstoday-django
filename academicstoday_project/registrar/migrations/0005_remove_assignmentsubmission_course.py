# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0004_auto_20150312_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentsubmission',
            name='course',
        ),
    ]
