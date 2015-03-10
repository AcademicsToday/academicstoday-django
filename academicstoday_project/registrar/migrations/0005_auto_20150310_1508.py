# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0004_auto_20150310_1447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursereviewsubmission',
            name='courses',
        ),
        migrations.AddField(
            model_name='coursereviewsubmission',
            name='course',
            field=models.ForeignKey(default=0, to='registrar.Course'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coursereviewsubmission',
            name='status',
            field=models.PositiveSmallIntegerField(default=2),
            preserve_default=True,
        ),
    ]
