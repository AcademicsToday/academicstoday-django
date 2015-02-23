# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_syllabus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='syllabus',
            name='file_url',
        ),
        migrations.AddField(
            model_name='syllabus',
            name='url',
            field=models.URLField(default=''),
            preserve_default=True,
        ),
    ]
