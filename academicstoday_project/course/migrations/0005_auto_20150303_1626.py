# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_auto_20150303_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='post_date',
            field=models.DateField(null=True, auto_now_add=True, auto_now=True),
            preserve_default=True,
        ),
    ]
