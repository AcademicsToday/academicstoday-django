# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0028_assignmentsubmission_student_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='submission_date',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
    ]
