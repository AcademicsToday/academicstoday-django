# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0017_auto_20150311_1331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='responsesubmission',
            name='course',
        ),
        migrations.RemoveField(
            model_name='responsesubmission',
            name='question_num',
        ),
        migrations.AddField(
            model_name='responsesubmission',
            name='question',
            field=models.ForeignKey(default=0, to='registrar.ResponseQuestion'),
            preserve_default=False,
        ),
    ]
