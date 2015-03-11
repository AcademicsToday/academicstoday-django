# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0016_auto_20150311_1251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='truefalsesubmission',
            name='course',
        ),
        migrations.RemoveField(
            model_name='truefalsesubmission',
            name='question_num',
        ),
        migrations.AddField(
            model_name='truefalsesubmission',
            name='exam',
            field=models.ForeignKey(null=True, to='registrar.Exam'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='truefalsesubmission',
            name='question',
            field=models.ForeignKey(to='registrar.TrueFalseQuestion', default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='truefalsesubmission',
            name='submission_id',
            field=models.AutoField(max_length=11, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
