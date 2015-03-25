# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landpage', '0003_landpagecontactmessage_name'),
    ]

    operations = [
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
        migrations.AlterField(
            model_name='coursepreview',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='landpagecoursepreview',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='landpageteammember',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
            preserve_default=True,
        ),
    ]
