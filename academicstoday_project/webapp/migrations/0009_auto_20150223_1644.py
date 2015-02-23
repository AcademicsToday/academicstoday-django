# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_lecture'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='lecture_num',
            field=models.IntegerField(default=0, max_length=7),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='description',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lecture',
            name='title',
            field=models.CharField(default='', max_length=31),
            preserve_default=True,
        ),
    ]
