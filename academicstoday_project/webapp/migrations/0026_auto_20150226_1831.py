# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0025_auto_20150226_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multiplechoicequestion',
            name='json_answers',
            field=models.CharField(max_length=127, default='{}'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='multiplechoicequestion',
            name='json_choices',
            field=models.CharField(max_length=1055, default='{}'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='multiplechoicesubmission',
            name='json_answers',
            field=models.CharField(max_length=127, default='{}'),
            preserve_default=True,
        ),
    ]
