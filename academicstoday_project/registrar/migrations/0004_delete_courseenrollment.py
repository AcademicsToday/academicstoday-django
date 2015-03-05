# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0003_student_courses'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CourseEnrollment',
        ),
    ]
