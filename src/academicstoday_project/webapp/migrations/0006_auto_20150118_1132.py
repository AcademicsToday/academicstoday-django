# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_landpage_team_member'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='landpage_team_member',
            table='at_landpage_team_members',
        ),
    ]
