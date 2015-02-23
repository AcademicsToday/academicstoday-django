# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_announcement'),
    ]

    operations = [
        migrations.CreateModel(
            name='Syllabus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, max_length=11)),
                ('course_id', models.IntegerField(max_length=11)),
                ('file_url', models.CharField(max_length=31)),
            ],
            options={
                'db_table': 'at_syllabus',
            },
            bases=(models.Model,),
        ),
    ]
