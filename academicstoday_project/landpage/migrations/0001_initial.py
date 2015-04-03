# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoursePreview',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image_filename', models.CharField(max_length=31)),
                ('title', models.CharField(max_length=63)),
                ('sub_title', models.CharField(max_length=127)),
                ('category', models.CharField(max_length=31)),
                ('description', models.TextField()),
                ('summary', models.TextField()),
            ],
            options={
                'db_table': 'at_course_previews',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LandpageContactMessage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=127)),
                ('email', models.EmailField(max_length=75)),
                ('phone', models.CharField(max_length=63)),
                ('message', models.TextField()),
            ],
            options={
                'db_table': 'at_landpage_contact_message',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LandpageCoursePreview',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
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
            name='LandpagePartner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image_filename', models.CharField(max_length=31)),
                ('title', models.CharField(max_length=127)),
                ('url', models.URLField()),
            ],
            options={
                'db_table': 'at_landpage_partners',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LandpageTeamMember',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=31)),
                ('role', models.CharField(max_length=31)),
                ('twitter_url', models.CharField(null=True, max_length=255)),
                ('facebook_url', models.CharField(null=True, max_length=255)),
                ('image_filename', models.CharField(null=True, max_length=255)),
                ('linkedin_url', models.CharField(null=True, max_length=255)),
                ('github_url', models.CharField(null=True, max_length=255)),
                ('google_url', models.CharField(null=True, max_length=255)),
                ('email', models.EmailField(null=True, max_length=75)),
            ],
            options={
                'db_table': 'at_landpage_team_members',
            },
            bases=(models.Model,),
        ),
    ]
