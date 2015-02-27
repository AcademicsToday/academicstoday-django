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
                ('id', models.AutoField(max_length=11, primary_key=True, serialize=False)),
                ('assignment_id', models.IntegerField(max_length=11)),
                ('student_id', models.BigIntegerField()),
                ('course_id', models.IntegerField(max_length=11)),
                ('order_num', models.SmallIntegerField(default=0)),
                ('type', models.SmallIntegerField()),
                ('submission_date', models.DateField(null=True)),
            ],
            options={
                'db_table': 'at_assignment_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelTable(
            name='multiplechoicequestion',
            table='at_multiple_choice_questions',
        ),
    ]
