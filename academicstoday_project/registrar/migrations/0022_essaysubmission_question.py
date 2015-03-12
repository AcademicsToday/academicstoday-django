# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0021_assignmentsubmission_is_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='essaysubmission',
            name='question',
            field=models.ForeignKey(default=0, to='registrar.EssayQuestion'),
            preserve_default=False,
        ),
    ]
