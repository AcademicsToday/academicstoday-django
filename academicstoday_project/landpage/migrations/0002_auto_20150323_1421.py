# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landpage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandpageContactMessage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('phone', models.CharField(max_length=63)),
                ('message', models.TextField()),
            ],
            options={
                'db_table': 'at_landpage_contact_message',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='landpageteammember',
            name='email',
            field=models.EmailField(max_length=75),
            preserve_default=True,
        ),
    ]
