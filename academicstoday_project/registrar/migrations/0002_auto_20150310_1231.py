# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='type',
        ),
        migrations.AddField(
            model_name='exam',
            name='description',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exam',
            name='title',
            field=models.CharField(max_length=31, null=True),
            preserve_default=True,
        ),
    ]
