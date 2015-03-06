# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20150305_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='file',
            field=models.FileField(upload_to='uploads', default=False),
            preserve_default=True,
        ),
    ]
