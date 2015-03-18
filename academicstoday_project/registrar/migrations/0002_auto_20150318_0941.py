# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseSetting',
            fields=[
                ('settings_id', models.AutoField(primary_key=True, serialize=False)),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_course_settings',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='exam',
            name='is_final',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
