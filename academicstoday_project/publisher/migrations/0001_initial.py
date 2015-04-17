# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('publication_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=127, null=True)),
                ('description', models.TextField(null=True)),
                ('published_date', models.DateField(auto_now=True, null=True)),
                ('file', models.FileField(upload_to='uploads', null=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('reviews', models.ManyToManyField(to='registrar.PeerReview')),
            ],
            options={
                'db_table': 'at_publications',
            },
        ),
    ]
