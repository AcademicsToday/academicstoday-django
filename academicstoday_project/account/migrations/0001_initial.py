# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateMessage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=127)),
                ('text', models.TextField()),
                ('sent_date', models.DateField(auto_now_add=True, null=True)),
                ('to_address', models.CharField(max_length=255)),
                ('from_address', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'at_private_messages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'at_students',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('teacher_id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'at_teachers',
            },
            bases=(models.Model,),
        ),
    ]
