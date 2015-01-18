# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landpage_team_member',
            name='email',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='landpage_team_member',
            name='facebook_url',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='landpage_team_member',
            name='full_name',
            field=models.CharField(max_length=31),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='landpage_team_member',
            name='image_filename',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='landpage_team_member',
            name='linkedin_url',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='landpage_team_member',
            name='role',
            field=models.CharField(max_length=31),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='landpage_team_member',
            name='twitter_url',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
