# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0017_auto_20150224_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='essaysubmission',
            name='file',
            field=models.FileField(upload_to='uploads', storage=django.core.files.storage.FileSystemStorage(location='uploads', base_url='/media/uploads'), blank=True, null=True),
            preserve_default=True,
        ),
    ]
