# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0002_auto_20150312_1529'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='essaysubmissionreview',
            name='assignment',
        ),
        migrations.RemoveField(
            model_name='essaysubmissionreview',
            name='course',
        ),
        migrations.RemoveField(
            model_name='essaysubmissionreview',
            name='exam',
        ),
        migrations.RemoveField(
            model_name='essaysubmissionreview',
            name='question',
        ),
        migrations.RemoveField(
            model_name='essaysubmissionreview',
            name='quiz',
        ),
    ]
