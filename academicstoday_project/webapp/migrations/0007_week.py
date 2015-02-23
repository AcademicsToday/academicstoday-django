# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_auto_20150223_1340'),
    ]

    operations = [
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(primary_key=True, max_length=11, serialize=False)),
                ('course_id', models.IntegerField(max_length=11)),
                ('week_num', models.IntegerField(max_length=7)),
                ('title', models.CharField(max_length=31)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'at_weeks',
            },
            bases=(models.Model,),
        ),
    ]
