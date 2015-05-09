# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landpage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='landpagecontactmessage',
            name='posted_date',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
    ]
