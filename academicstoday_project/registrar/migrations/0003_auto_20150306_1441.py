# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0002_remove_syllabus_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='policy',
            name='course_id',
        ),
        migrations.RemoveField(
            model_name='policy',
            name='url',
        ),
        migrations.AddField(
            model_name='policy',
            name='course',
            field=models.ForeignKey(default=0, to='registrar.Course'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='policy',
            name='file',
            field=models.FileField(upload_to='uploads', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='policy',
            name='policy_id',
            field=models.AutoField(primary_key=True, serialize=False),
            preserve_default=True,
        ),
    ]
