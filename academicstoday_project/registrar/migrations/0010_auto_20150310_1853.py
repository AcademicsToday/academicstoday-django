# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0009_auto_20150310_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='preferred_service',
            field=models.CharField(default=1, choices=[(1, 'YouTube'), (2, 'Vimeo')], max_length=1),
            preserve_default=True,
        ),
    ]
