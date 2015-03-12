# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0005_remove_assignmentsubmission_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examsubmission',
            name='course',
        ),
        migrations.RemoveField(
            model_name='quizsubmission',
            name='course',
        ),
    ]
