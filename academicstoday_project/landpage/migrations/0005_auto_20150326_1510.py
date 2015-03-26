# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landpage', '0004_auto_20150325_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='landpageteammember',
            name='github_url',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='landpageteammember',
            name='google_url',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
