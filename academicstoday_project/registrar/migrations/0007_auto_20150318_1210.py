# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0006_auto_20150318_1129'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignmentsubmission',
            old_name='score',
            new_name='earned_marks',
        ),
        migrations.RemoveField(
            model_name='assignmentsubmission',
            name='is_marked',
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='percent',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='total_marks',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='essayquestion',
            name='question_num',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='multiplechoicequestion',
            name='marks',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='responsequestion',
            name='marks',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='truefalsequestion',
            name='marks',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], default=1),
            preserve_default=True,
        ),
    ]
