# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0007_auto_20150318_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='earned_marks',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='percent',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='essaysubmission',
            name='marks',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='multiplechoicesubmission',
            name='marks',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='responsesubmission',
            name='marks',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='truefalsesubmission',
            name='marks',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
