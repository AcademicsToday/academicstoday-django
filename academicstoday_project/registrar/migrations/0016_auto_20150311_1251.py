# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0015_auto_20150311_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='multiplechoicesubmission',
            name='assignment',
            field=models.ForeignKey(to='registrar.Assignment', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicesubmission',
            name='exam',
            field=models.ForeignKey(to='registrar.Exam', null=True),
            preserve_default=True,
        ),
    ]
