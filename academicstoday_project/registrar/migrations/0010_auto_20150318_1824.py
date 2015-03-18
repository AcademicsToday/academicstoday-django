# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0009_auto_20150318_1756'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examsubmission',
            old_name='marks',
            new_name='total_marks',
        ),
        migrations.RemoveField(
            model_name='examsubmission',
            name='is_marked',
        ),
        migrations.AddField(
            model_name='examsubmission',
            name='earned_marks',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='examsubmission',
            name='percent',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
