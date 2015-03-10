# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0003_coursereview'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CourseReview',
            new_name='CourseReviewSubmission',
        ),
        migrations.AlterModelTable(
            name='coursereviewsubmission',
            table='at_course_review_submissions',
        ),
    ]
