# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0014_remove_assignmentsubmission_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='multiplechoicesubmission',
            name='assignment',
        ),
        migrations.RemoveField(
            model_name='multiplechoicesubmission',
            name='course',
        ),
        migrations.RemoveField(
            model_name='multiplechoicesubmission',
            name='exam',
        ),
        migrations.RemoveField(
            model_name='multiplechoicesubmission',
            name='json_answers',
        ),
        migrations.RemoveField(
            model_name='multiplechoicesubmission',
            name='question_num',
        ),
        migrations.AddField(
            model_name='multiplechoicesubmission',
            name='a',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicesubmission',
            name='b',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicesubmission',
            name='c',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicesubmission',
            name='d',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicesubmission',
            name='e',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicesubmission',
            name='f',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicesubmission',
            name='question',
            field=models.ForeignKey(default=9, to='registrar.MultipleChoiceQuestion'),
            preserve_default=False,
        ),
    ]
