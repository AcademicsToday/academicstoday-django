# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_auto_20150306_1028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='courses',
        ),
        migrations.AddField(
            model_name='announcement',
            name='course',
            field=models.ForeignKey(to='course.Course', default=1),
            preserve_default=False,
        ),
    ]
