# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_auto_20150305_2230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='is_available',
        ),
        migrations.AddField(
            model_name='course',
            name='status',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='file',
            field=models.FileField(null=True, upload_to='uploads'),
            preserve_default=True,
        ),
    ]
