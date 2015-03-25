# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursesetting',
            name='course_percent',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], default=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coursesetting',
            name='final_exam_percent',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], default=50),
            preserve_default=True,
        ),
    ]
