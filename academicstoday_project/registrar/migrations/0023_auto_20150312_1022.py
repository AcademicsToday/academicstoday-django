# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0022_essaysubmission_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizsubmission',
            name='quiz_id',
        ),
        migrations.RemoveField(
            model_name='quizsubmission',
            name='quiz_num',
        ),
        migrations.RemoveField(
            model_name='quizsubmission',
            name='type',
        ),
        migrations.AddField(
            model_name='quizsubmission',
            name='is_finished',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quizsubmission',
            name='quiz',
            field=models.ForeignKey(to='registrar.Quiz', default=0),
            preserve_default=False,
        ),
    ]
