# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0026_auto_20150226_1831'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignmentSubmission',
            fields=[
                ('assignment_id', models.AutoField(serialize=False, primary_key=True)),
                ('course_id', models.IntegerField(max_length=11)),
                ('order_num', models.SmallIntegerField(default=0)),
                ('type', models.SmallIntegerField()),
                ('submission_date', models.DateField(auto_now=True, null=True, auto_now_add=True)),
            ],
            options={
                'db_table': 'at_assignment_submissions',
            },
            bases=(models.Model,),
        ),
    ]
