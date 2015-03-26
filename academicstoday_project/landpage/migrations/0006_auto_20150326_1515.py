# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landpage', '0005_auto_20150326_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landpageteammember',
            name='facebook_url',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='landpageteammember',
            name='github_url',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='landpageteammember',
            name='google_url',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='landpageteammember',
            name='image_filename',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='landpageteammember',
            name='linkedin_url',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='landpageteammember',
            name='twitter_url',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
    ]
