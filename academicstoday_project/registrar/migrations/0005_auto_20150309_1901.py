# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0004_auto_20150307_1544'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='type',
        ),
        migrations.AddField(
            model_name='quiz',
            name='description',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='start_date',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='title',
            field=models.CharField(max_length=31, null=True),
            preserve_default=True,
        ),
    ]
