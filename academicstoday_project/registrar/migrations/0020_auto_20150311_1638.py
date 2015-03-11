# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0019_auto_20150311_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='submission_date',
            field=models.DateTimeField(null=True, auto_now=True),
            preserve_default=True,
        ),
    ]
