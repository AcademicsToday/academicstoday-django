# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0028_truefalsequestion_truefalsesubmission'),
    ]

    operations = [
        migrations.RenameField(
            model_name='responsesubmission',
            old_name='user_id',
            new_name='student_id',
        ),
        migrations.AddField(
            model_name='responsequestion',
            name='answer',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='responsesubmission',
            name='question_num',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
