# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0020_essaysubmission_submission_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='multiplechoicesubmission',
            old_name='user_id',
            new_name='student_id',
        ),
        migrations.AddField(
            model_name='multiplechoicesubmission',
            name='question_num',
            field=models.SmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
