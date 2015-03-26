# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landpage', '0006_auto_20150326_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landpageteammember',
            name='email',
            field=models.EmailField(max_length=75, null=True),
            preserve_default=True,
        ),
    ]
