# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0016_auto_20150224_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='essaysubmission',
            name='file',
            field=models.FileField(null=True, blank=True, upload_to='uploads'),
            preserve_default=True,
        ),
    ]
