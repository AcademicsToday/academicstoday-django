# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0003_auto_20150325_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursefinalmark',
            name='is_public',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
