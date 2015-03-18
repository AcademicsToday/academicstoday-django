# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0003_auto_20150318_0948'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignmentsubmission',
            old_name='marks',
            new_name='score',
        ),
    ]
