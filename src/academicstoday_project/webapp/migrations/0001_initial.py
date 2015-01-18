# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='landpage_team_member',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True, max_length=11)),
                ('full_name', models.CharField(max_length=200)),
                ('role', models.CharField(max_length=200)),
                ('twitter_url', models.CharField(max_length=200)),
                ('facebook_url', models.CharField(max_length=200)),
                ('image_filename', models.CharField(max_length=200)),
                ('linkedin_url', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
