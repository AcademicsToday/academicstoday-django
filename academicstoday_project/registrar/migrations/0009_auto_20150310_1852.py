# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0008_auto_20150310_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='bliptv_url',
            field=models.URLField(default='', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='description',
            field=models.TextField(default='', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='preferred_service',
            field=models.CharField(choices=[(1, 'YouTube'), (2, 'Vimeo')], max_length=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='title',
            field=models.CharField(default='', max_length=31, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='vimeo_url',
            field=models.URLField(default='', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='youtube_url',
            field=models.URLField(default='', blank=True, null=True),
            preserve_default=True,
        ),
    ]
