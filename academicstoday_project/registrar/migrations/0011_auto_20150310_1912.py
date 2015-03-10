# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0010_auto_20150310_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='description',
            field=models.TextField(default='', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='preferred_service',
            field=models.CharField(choices=[('1', 'YouTube'), ('2', 'Vimeo')], default='1', max_length=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='title',
            field=models.CharField(default='', null=True, max_length=31),
            preserve_default=True,
        ),
    ]
