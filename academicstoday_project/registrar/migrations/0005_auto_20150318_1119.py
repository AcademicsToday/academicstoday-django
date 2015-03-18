# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0004_auto_20150318_1108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='essaysubmission',
            name='is_marked',
        ),
        migrations.RemoveField(
            model_name='multiplechoicesubmission',
            name='is_marked',
        ),
        migrations.RemoveField(
            model_name='responsesubmission',
            name='is_marked',
        ),
        migrations.RemoveField(
            model_name='truefalsesubmission',
            name='is_marked',
        ),
        migrations.AddField(
            model_name='essayquestion',
            name='marks',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='essaysubmission',
            name='marks',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='marks',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='responsequestion',
            name='marks',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='truefalsequestion',
            name='marks',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=True,
        ),
    ]
