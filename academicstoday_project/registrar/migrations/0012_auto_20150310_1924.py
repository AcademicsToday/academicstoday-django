# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0011_auto_20150310_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='bliptv_url',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='vimeo_url',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='youtube_url',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
