# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0013_auto_20150310_1952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentsubmission',
            name='type',
        ),
    ]
