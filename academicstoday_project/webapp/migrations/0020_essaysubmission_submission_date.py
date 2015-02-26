# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0019_auto_20150225_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='essaysubmission',
            name='submission_date',
            field=models.DateTimeField(auto_now_add=True, auto_now=True, null=True),
            preserve_default=True,
        ),
    ]
