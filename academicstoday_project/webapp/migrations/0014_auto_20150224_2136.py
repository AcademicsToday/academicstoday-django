# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0013_auto_20150224_2100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='essaysubmission',
            name='course_id',
        ),
        migrations.RemoveField(
            model_name='essaysubmission',
            name='user_id',
        ),
        migrations.AlterField(
            model_name='essaysubmission',
            name='file',
            field=models.FileField(upload_to='uploads/%Y/%m/%d', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='essaysubmission',
            name='id',
            field=models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True),
            preserve_default=True,
        ),
    ]
