# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0027_assignmentsubmission'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsubmission',
            name='student_id',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
    ]
