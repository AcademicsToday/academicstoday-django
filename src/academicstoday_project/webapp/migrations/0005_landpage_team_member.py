# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_delete_landpage_team_member'),
    ]

    operations = [
        migrations.CreateModel(
            name='landpage_team_member',
            fields=[
                ('id', models.IntegerField(primary_key=True, max_length=11, serialize=False)),
                ('full_name', models.CharField(max_length=31)),
                ('role', models.CharField(max_length=31)),
                ('twitter_url', models.CharField(max_length=255)),
                ('facebook_url', models.CharField(max_length=255)),
                ('image_filename', models.CharField(max_length=255)),
                ('linkedin_url', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'team_member',
                'db_table': 'landpage_team_members',
                'verbose_name_plural': 'team_members',
            },
            bases=(models.Model,),
        ),
    ]
