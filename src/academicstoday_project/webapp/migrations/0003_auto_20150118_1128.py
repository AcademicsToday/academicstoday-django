# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20150118_1116'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='landpage_team_member',
            options={'verbose_name': 'landpage_team_member', 'verbose_name_plural': 'landpage_team_members'},
        ),
    ]
