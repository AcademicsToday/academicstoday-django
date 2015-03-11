# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0018_auto_20150311_1443'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentsubmission',
            name='assignment_num',
        ),
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='submission_date',
            field=models.DateTimeField(auto_now=True, auto_now_add=True, null=True),
            preserve_default=True,
        ),
    ]
