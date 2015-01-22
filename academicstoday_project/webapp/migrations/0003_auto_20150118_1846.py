# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_coursepreivew'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CoursePreivew',
            new_name='CoursePreview',
        ),
    ]
