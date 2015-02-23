# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_policy'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='policy',
            table='at_policys',
        ),
    ]
