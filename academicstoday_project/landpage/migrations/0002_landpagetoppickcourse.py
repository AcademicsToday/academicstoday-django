# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0001_initial'),
        ('landpage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandpageTopPickCourse',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_landpage_top_pick_courses',
            },
            bases=(models.Model,),
        ),
    ]
