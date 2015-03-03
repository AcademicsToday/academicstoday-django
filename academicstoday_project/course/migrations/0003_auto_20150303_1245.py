# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20150303_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsubmission',
            name='is_marked',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='essaysubmission',
            name='is_marked',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='examsubmission',
            name='is_marked',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicesubmission',
            name='is_marked',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quizsubmission',
            name='is_marked',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='responsesubmission',
            name='is_marked',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='truefalsesubmission',
            name='is_marked',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
