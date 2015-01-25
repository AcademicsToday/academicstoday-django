# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20150118_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, max_length=11, serialize=False)),
                ('image_filename', models.CharField(max_length=31)),
                ('title', models.CharField(max_length=63)),
                ('sub_title', models.CharField(max_length=127)),
                ('category', models.CharField(max_length=31)),
                ('description', models.TextField()),
                ('summary', models.TextField()),
            ],
            options={
                'db_table': 'at_courses',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='coursepreview',
            name='id',
            field=models.AutoField(primary_key=True, max_length=11, serialize=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='landpagecoursepreview',
            name='id',
            field=models.AutoField(primary_key=True, max_length=11, serialize=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='landpageteammember',
            name='id',
            field=models.AutoField(primary_key=True, max_length=11, serialize=False),
            preserve_default=True,
        ),
    ]
