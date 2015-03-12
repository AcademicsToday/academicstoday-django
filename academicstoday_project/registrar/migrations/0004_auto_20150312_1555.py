# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0003_auto_20150312_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='essayquestion',
            name='course',
        ),
        migrations.RemoveField(
            model_name='essaysubmission',
            name='assignment',
        ),
        migrations.RemoveField(
            model_name='essaysubmission',
            name='course',
        ),
        migrations.RemoveField(
            model_name='essaysubmission',
            name='exam',
        ),
        migrations.RemoveField(
            model_name='essaysubmission',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='multiplechoicequestion',
            name='course',
        ),
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
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='responsequestion',
            name='course',
        ),
        migrations.RemoveField(
            model_name='responsesubmission',
            name='assignment',
        ),
        migrations.RemoveField(
            model_name='responsesubmission',
            name='course',
        ),
        migrations.RemoveField(
            model_name='responsesubmission',
            name='exam',
        ),
        migrations.RemoveField(
            model_name='responsesubmission',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='truefalsequestion',
            name='course',
        ),
        migrations.RemoveField(
            model_name='truefalsesubmission',
            name='assignment',
        ),
        migrations.RemoveField(
            model_name='truefalsesubmission',
            name='course',
        ),
        migrations.RemoveField(
            model_name='truefalsesubmission',
            name='exam',
        ),
        migrations.RemoveField(
            model_name='truefalsesubmission',
            name='quiz',
        ),
    ]
