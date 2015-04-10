# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0004_auto_20150409_0944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='file',
        ),
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(null=True, upload_to='uploads'),
        ),
    ]
