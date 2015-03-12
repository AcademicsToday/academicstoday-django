# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0023_auto_20150312_1022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examsubmission',
            name='exam_num',
        ),
        migrations.RemoveField(
            model_name='examsubmission',
            name='type',
        ),
        migrations.AddField(
            model_name='examsubmission',
            name='is_finished',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
