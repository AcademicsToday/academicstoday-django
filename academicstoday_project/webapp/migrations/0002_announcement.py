# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(serialize=False, max_length=11, primary_key=True)),
                ('course_id', models.IntegerField(max_length=11)),
                ('title', models.CharField(max_length=31)),
                ('body', models.TextField()),
                ('post_date', models.DateField()),
            ],
            options={
                'db_table': 'at_announcements',
            },
            bases=(models.Model,),
        ),
    ]
