# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landpage', '0002_auto_20150323_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='landpagecontactmessage',
            name='name',
            field=models.CharField(max_length=127, default=0),
            preserve_default=False,
        ),
    ]
