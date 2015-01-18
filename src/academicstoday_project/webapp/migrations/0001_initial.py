# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LandpageCoursePreview',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True, max_length=11)),
                ('image_filename', models.CharField(max_length=31)),
                ('title', models.CharField(max_length=127)),
                ('category', models.CharField(max_length=31)),
            ],
            options={
                'db_table': 'at_landpage_course_previews',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LandpageTeamMember',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True, max_length=11)),
                ('full_name', models.CharField(max_length=31)),
                ('role', models.CharField(max_length=31)),
                ('twitter_url', models.CharField(max_length=255)),
                ('facebook_url', models.CharField(max_length=255)),
                ('image_filename', models.CharField(max_length=255)),
                ('linkedin_url', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'at_landpage_team_members',
            },
            bases=(models.Model,),
        ),
    ]
