# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0021_auto_20150226_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='multiplechoicesubmission',
            name='submission_date',
            field=models.DateTimeField(auto_now=True, null=True, auto_now_add=True),
            preserve_default=True,
        ),
    ]
