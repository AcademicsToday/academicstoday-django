# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0012_assignment_order_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='essaysubmission',
            name='file_path',
        ),
        migrations.AddField(
            model_name='essaysubmission',
            name='file',
            field=models.FileField(upload_to='', null=True),
            preserve_default=True,
        ),
    ]
