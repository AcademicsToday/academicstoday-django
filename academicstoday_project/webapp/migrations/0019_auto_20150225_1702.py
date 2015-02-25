# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0018_auto_20150224_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='essaysubmission',
            name='course_id',
            field=models.IntegerField(max_length=11, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='essaysubmission',
            name='student_id',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='essaysubmission',
            name='assignment_id',
            field=models.BigIntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='essaysubmission',
            name='file',
            field=models.FileField(upload_to='uploads', default=1),
            preserve_default=False,
        ),
    ]
