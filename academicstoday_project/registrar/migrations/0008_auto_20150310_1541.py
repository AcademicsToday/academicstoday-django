# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0007_auto_20150310_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursesubmission',
            name='from_reviewer',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='coursesubmission',
            name='from_submitter',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
