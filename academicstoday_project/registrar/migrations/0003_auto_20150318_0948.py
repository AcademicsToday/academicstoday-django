# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0002_auto_20150318_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='worth',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, '0 %'), (10, '10 %'), (15, '15 %'), (20, '20 %'), (25, '25 %'), (30, '30 %'), (35, '35 %'), (40, '40 %'), (45, '45 %'), (50, '50 %'), (55, '55 %'), (60, '60 %'), (65, '65 %'), (70, '70 %'), (75, '75 %'), (80, '80 %'), (85, '85 %'), (90, '90 %'), (95, '95 %'), (100, '100 %')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exam',
            name='worth',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, '0 %'), (10, '10 %'), (15, '15 %'), (20, '20 %'), (25, '25 %'), (30, '30 %'), (35, '35 %'), (40, '40 %'), (45, '45 %'), (50, '50 %'), (55, '55 %'), (60, '60 %'), (65, '65 %'), (70, '70 %'), (75, '75 %'), (80, '80 %'), (85, '85 %'), (90, '90 %'), (95, '95 %'), (100, '100 %')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='worth',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, '0 %'), (10, '10 %'), (15, '15 %'), (20, '20 %'), (25, '25 %'), (30, '30 %'), (35, '35 %'), (40, '40 %'), (45, '45 %'), (50, '50 %'), (55, '55 %'), (60, '60 %'), (65, '65 %'), (70, '70 %'), (75, '75 %'), (80, '80 %'), (85, '85 %'), (90, '90 %'), (95, '95 %'), (100, '100 %')]),
            preserve_default=True,
        ),
    ]
