# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_auto_20150306_1103'),
    ]

    operations = [
        migrations.RenameField(
            model_name='announcement',
            old_name='id',
            new_name='announcement_id',
        ),
    ]
