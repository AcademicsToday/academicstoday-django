# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0002_auto_20150408_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('upload_id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=127, null=True)),
                ('title', models.CharField(max_length=127, null=True)),
                ('description', models.TextField(null=True)),
                ('upload_date', models.DateField(null=True, auto_now=True)),
                ('file', models.FileField(null=True, upload_to='uploads')),
            ],
            options={
                'db_table': 'at_file_uploads',
            },
        ),
        migrations.RemoveField(
            model_name='pdfupload',
            name='user',
        ),
        migrations.AlterField(
            model_name='lecture',
            name='notes',
            field=models.ManyToManyField(to='registrar.FileUpload'),
        ),
        migrations.DeleteModel(
            name='PDFUpload',
        ),
    ]
