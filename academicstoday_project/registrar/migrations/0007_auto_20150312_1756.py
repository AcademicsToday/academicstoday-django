# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registrar', '0006_auto_20150312_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeerReview',
            fields=[
                ('review_id', models.AutoField(max_length=11, serialize=False, primary_key=True)),
                ('marks', models.PositiveSmallIntegerField(default=0, choices=[(0, '0 Star'), (1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])),
                ('text', models.TextField(null=True, blank=True)),
                ('date', models.DateTimeField(null=True, auto_now=True, auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'at_peer_reviews',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='essaysubmissionreview',
            name='student',
        ),
        migrations.RemoveField(
            model_name='essaysubmissionreview',
            name='submission',
        ),
        migrations.DeleteModel(
            name='EssaySubmissionReview',
        ),
        migrations.AddField(
            model_name='essaysubmission',
            name='reviews',
            field=models.ManyToManyField(to='registrar.PeerReview'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='responsesubmission',
            name='reviews',
            field=models.ManyToManyField(to='registrar.PeerReview'),
            preserve_default=True,
        ),
    ]
