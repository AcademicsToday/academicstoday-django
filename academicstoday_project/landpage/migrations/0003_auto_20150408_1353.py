# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landpage', '0002_landpagetoppickcourse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landpagecontactmessage',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='landpageteammember',
            name='email',
            field=models.EmailField(null=True, max_length=254),
        ),
    ]
