# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registrar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PDFUpload',
            fields=[
                ('upload_id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(null=True, max_length=127)),
                ('title', models.CharField(null=True, max_length=127)),
                ('description', models.TextField(null=True)),
                ('upload_date', models.DateField(null=True, auto_now=True)),
                ('file', models.FileField(null=True, upload_to='uploads')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'at_pdf_uploads',
            },
        ),
        migrations.AlterField(
            model_name='announcement',
            name='post_date',
            field=models.DateField(null=True, auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='coursediscussionpost',
            name='date',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
        migrations.AlterField(
            model_name='coursediscussionthread',
            name='date',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
        migrations.AlterField(
            model_name='coursesubmission',
            name='submission_date',
            field=models.DateField(null=True, auto_now=True),
        ),
        migrations.AlterField(
            model_name='essaysubmission',
            name='submission_date',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
        migrations.AlterField(
            model_name='examsubmission',
            name='submission_date',
            field=models.DateField(null=True, auto_now=True),
        ),
        migrations.AlterField(
            model_name='multiplechoicesubmission',
            name='submission_date',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
        migrations.AlterField(
            model_name='peerreview',
            name='date',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
        migrations.AlterField(
            model_name='quizsubmission',
            name='submission_date',
            field=models.DateField(null=True, auto_now=True),
        ),
        migrations.AlterField(
            model_name='responsesubmission',
            name='submission_date',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
        migrations.AlterField(
            model_name='truefalsesubmission',
            name='submission_date',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
        migrations.AddField(
            model_name='lecture',
            name='notes',
            field=models.ManyToManyField(to='registrar.PDFUpload'),
        ),
    ]
