# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20150118_1128'),
    ]

    operations = [
        migrations.DeleteModel(
            name='landpage_team_member',
        ),
    ]
