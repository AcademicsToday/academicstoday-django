# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0011_auto_20150224_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='order_num',
            field=models.SmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
