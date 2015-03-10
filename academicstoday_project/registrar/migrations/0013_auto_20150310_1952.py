# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0012_auto_20150310_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multiplechoicequestion',
            name='c',
            field=models.CharField(max_length=255, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='multiplechoicequestion',
            name='d',
            field=models.CharField(max_length=255, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='multiplechoicequestion',
            name='e',
            field=models.CharField(max_length=255, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='multiplechoicequestion',
            name='f',
            field=models.CharField(max_length=255, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='multiplechoicequestion',
            name='title',
            field=models.CharField(max_length=31, default='', blank=True),
            preserve_default=True,
        ),
    ]
