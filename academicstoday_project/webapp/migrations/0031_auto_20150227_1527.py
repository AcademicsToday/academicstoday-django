# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0030_auto_20150227_1454'),
    ]

    operations = [
        migrations.RenameField(
            model_name='responsesubmission',
            old_name='response',
            new_name='answer',
        ),
    ]
