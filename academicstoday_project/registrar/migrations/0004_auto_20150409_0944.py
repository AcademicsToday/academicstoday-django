# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0003_auto_20150409_0925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileupload',
            name='category',
        ),
        migrations.AddField(
            model_name='fileupload',
            name='type',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
