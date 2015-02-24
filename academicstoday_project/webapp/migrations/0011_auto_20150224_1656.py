# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_auto_20150224_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='due_date',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='bliptv_url',
            field=models.URLField(null=True, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='description',
            field=models.TextField(null=True, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='title',
            field=models.CharField(null=True, max_length=31, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='vimeo_url',
            field=models.URLField(null=True, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='youtube_url',
            field=models.URLField(null=True, default=''),
            preserve_default=True,
        ),
    ]
