# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_auto_20150305_2227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='image',
            new_name='file',
        ),
    ]
