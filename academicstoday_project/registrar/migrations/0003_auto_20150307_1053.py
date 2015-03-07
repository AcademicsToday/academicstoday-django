# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0002_auto_20150306_1922'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='type',
        ),
        migrations.AddField(
            model_name='assignment',
            name='start_date',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
    ]
