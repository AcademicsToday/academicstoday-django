# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20150303_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.CharField(max_length=31, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='finish_date',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='image_filename',
            field=models.CharField(max_length=31, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='paragraph_one',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='paragraph_three',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='paragraph_two',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='start_date',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='sub_title',
            field=models.CharField(max_length=127, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(max_length=63, null=True),
            preserve_default=True,
        ),
    ]
