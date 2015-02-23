# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20150223_1235'),
    ]

    operations = [
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(primary_key=True, max_length=11, serialize=False)),
                ('course_id', models.IntegerField(max_length=11)),
                ('url', models.URLField(default='')),
            ],
            options={
                'db_table': 'at_policy',
            },
            bases=(models.Model,),
        ),
    ]
