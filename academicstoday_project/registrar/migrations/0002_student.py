# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('registrar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'at_students',
            },
            bases=(models.Model,),
        ),
    ]
