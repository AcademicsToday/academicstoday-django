# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0022_multiplechoicesubmission_submission_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MultipleChoiceAnswer',
        ),
        migrations.DeleteModel(
            name='MultipleChoiceOption',
        ),
        migrations.RemoveField(
            model_name='multiplechoicesubmission',
            name='selected',
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='a_choice',
            field=models.CharField(null=True, max_length=63),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='answer',
            field=models.CharField(null=True, max_length=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='b_choice',
            field=models.CharField(null=True, max_length=63),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='c_choice',
            field=models.CharField(null=True, max_length=63),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='d_choice',
            field=models.CharField(null=True, max_length=63),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='e_choice',
            field=models.CharField(null=True, max_length=63),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='f_choice',
            field=models.CharField(null=True, max_length=63),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='g_choice',
            field=models.CharField(null=True, max_length=63),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='h_choice',
            field=models.CharField(null=True, max_length=63),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='i_choice',
            field=models.CharField(null=True, max_length=63),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='j_choice',
            field=models.CharField(null=True, max_length=63),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicesubmission',
            name='answer',
            field=models.CharField(null=True, max_length=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicesubmission',
            name='is_correct',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterModelTable(
            name='responsequestion',
            table='at_response_questions',
        ),
    ]
