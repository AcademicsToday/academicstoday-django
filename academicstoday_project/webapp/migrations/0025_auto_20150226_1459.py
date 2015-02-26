# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0024_auto_20150226_1447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='multiplechoicesubmission',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='multiplechoicesubmission',
            name='is_correct',
        ),
        migrations.AddField(
            model_name='multiplechoicesubmission',
            name='json_answers',
            field=models.CharField(null=True, max_length=127),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicesubmission',
            name='marks',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
