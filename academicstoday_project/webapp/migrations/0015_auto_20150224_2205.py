# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0014_auto_20150224_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='essaysubmission',
            name='file',
            field=models.FileField(null=True, upload_to='uploads/'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='essaysubmission',
            name='id',
            field=models.AutoField(serialize=False, max_length=11, primary_key=True),
            preserve_default=True,
        ),
    ]
