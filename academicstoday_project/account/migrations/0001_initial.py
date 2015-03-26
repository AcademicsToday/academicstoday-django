# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateMessage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=127)),
                ('text', models.TextField()),
                ('sent_date', models.DateField(null=True, auto_now_add=True)),
                ('to_address', models.CharField(max_length=255)),
                ('from_address', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'at_private_messages',
            },
            bases=(models.Model,),
        ),
    ]
