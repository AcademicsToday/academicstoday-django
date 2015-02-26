# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0023_auto_20150226_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='multiplechoicequestion',
            name='a_choice',
        ),
        migrations.RemoveField(
            model_name='multiplechoicequestion',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='multiplechoicequestion',
            name='b_choice',
        ),
        migrations.RemoveField(
            model_name='multiplechoicequestion',
            name='c_choice',
        ),
        migrations.RemoveField(
            model_name='multiplechoicequestion',
            name='d_choice',
        ),
        migrations.RemoveField(
            model_name='multiplechoicequestion',
            name='e_choice',
        ),
        migrations.RemoveField(
            model_name='multiplechoicequestion',
            name='f_choice',
        ),
        migrations.RemoveField(
            model_name='multiplechoicequestion',
            name='g_choice',
        ),
        migrations.RemoveField(
            model_name='multiplechoicequestion',
            name='h_choice',
        ),
        migrations.RemoveField(
            model_name='multiplechoicequestion',
            name='i_choice',
        ),
        migrations.RemoveField(
            model_name='multiplechoicequestion',
            name='j_choice',
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='json_answers',
            field=models.CharField(null=True, max_length=127),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='json_choices',
            field=models.CharField(null=True, max_length=1055),
            preserve_default=True,
        ),
    ]
