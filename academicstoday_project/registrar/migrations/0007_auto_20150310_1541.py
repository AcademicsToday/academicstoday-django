# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0006_auto_20150310_1535'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursesubmission',
            old_name='review',
            new_name='from_reviewer',
        ),
        migrations.AddField(
            model_name='coursesubmission',
            name='from_submitter',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
