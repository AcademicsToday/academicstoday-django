# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_course_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='file',
            new_name='image',
        ),
    ]
