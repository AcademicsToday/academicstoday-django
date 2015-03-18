# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0005_auto_20150318_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='essayquestion',
            name='marks',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='essayquestion',
            name='question_id',
            field=models.AutoField(serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
