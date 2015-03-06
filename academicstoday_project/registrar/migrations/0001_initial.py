# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('announcement_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=31)),
                ('body', models.TextField()),
                ('post_date', models.DateField(auto_now=True, auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'at_announcements',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('assignment_id', models.AutoField(serialize=False, primary_key=True, max_length=11)),
                ('course_id', models.PositiveIntegerField()),
                ('order_num', models.PositiveSmallIntegerField(default=0)),
                ('type', models.PositiveSmallIntegerField()),
                ('due_date', models.DateField(null=True)),
            ],
            options={
                'db_table': 'at_assignments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AssignmentReview',
            fields=[
                ('review_id', models.AutoField(serialize=False, primary_key=True, max_length=11)),
                ('student_id', models.BigIntegerField()),
                ('assignment_id', models.PositiveIntegerField()),
                ('course_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=31)),
                ('comment', models.TextField()),
                ('marks', models.PositiveSmallIntegerField(default=0)),
                ('post_date', models.DateField(auto_now=True, auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'at_assignment_reviews',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AssignmentSubmission',
            fields=[
                ('submission_id', models.AutoField(serialize=False, primary_key=True, max_length=11)),
                ('assignment_id', models.PositiveIntegerField()),
                ('student_id', models.BigIntegerField()),
                ('course_id', models.PositiveIntegerField()),
                ('order_num', models.PositiveSmallIntegerField(default=0)),
                ('type', models.PositiveSmallIntegerField()),
                ('marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateField(null=True)),
                ('is_marked', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'at_assignment_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=127)),
                ('sub_title', models.CharField(max_length=127)),
                ('category', models.CharField(max_length=127)),
                ('description', models.TextField(null=True)),
                ('start_date', models.DateField(null=True)),
                ('finish_date', models.DateField(null=True)),
                ('is_official', models.BooleanField(default=False)),
                ('status', models.PositiveSmallIntegerField(default=0)),
                ('file', models.FileField(upload_to='uploads', null=True)),
            ],
            options={
                'db_table': 'at_courses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EssayQuestion',
            fields=[
                ('question_id', models.AutoField(serialize=False, primary_key=True, max_length=11)),
                ('assignment_id', models.PositiveIntegerField()),
                ('course_id', models.PositiveIntegerField()),
                ('question_num', models.PositiveSmallIntegerField()),
                ('title', models.CharField(max_length=31, default='')),
                ('description', models.TextField(default='')),
            ],
            options={
                'db_table': 'at_essay_questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EssaySubmission',
            fields=[
                ('submission_id', models.AutoField(serialize=False, primary_key=True, max_length=11)),
                ('assignment_id', models.BigIntegerField()),
                ('student_id', models.BigIntegerField()),
                ('course_id', models.PositiveIntegerField()),
                ('file', models.FileField(upload_to='uploads')),
                ('submission_date', models.DateTimeField(auto_now=True, auto_now_add=True, null=True)),
                ('is_marked', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'at_essay_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('exam_id', models.AutoField(serialize=False, primary_key=True, max_length=11)),
                ('course_id', models.PositiveIntegerField()),
                ('order_num', models.PositiveSmallIntegerField(default=0)),
                ('type', models.PositiveSmallIntegerField()),
                ('start_date', models.DateField(null=True)),
                ('due_date', models.DateField(null=True)),
            ],
            options={
                'db_table': 'at_exams',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExamSubmission',
            fields=[
                ('submission_id', models.AutoField(serialize=False, primary_key=True, max_length=11)),
                ('exam_id', models.PositiveIntegerField()),
                ('student_id', models.BigIntegerField()),
                ('course_id', models.PositiveIntegerField()),
                ('order_num', models.PositiveSmallIntegerField(default=0)),
                ('type', models.PositiveSmallIntegerField()),
                ('marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateField(null=True)),
                ('is_marked', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'at_exam_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('lecture_id', models.AutoField(serialize=False, primary_key=True, max_length=11)),
                ('course_id', models.PositiveIntegerField()),
                ('week_num', models.PositiveSmallIntegerField(max_length=7)),
                ('lecture_num', models.PositiveSmallIntegerField(max_length=7, default=0)),
                ('title', models.CharField(max_length=31, default='', null=True)),
                ('description', models.TextField(default='', null=True)),
                ('youtube_url', models.URLField(default='', null=True)),
                ('vimeo_url', models.URLField(default='', null=True)),
                ('bliptv_url', models.URLField(default='', null=True)),
                ('preferred_service', models.CharField(max_length=31)),
            ],
            options={
                'db_table': 'at_lectures',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('question_id', models.AutoField(serialize=False, primary_key=True, max_length=11)),
                ('exam_id', models.PositiveIntegerField(default=0)),
                ('assignment_id', models.PositiveIntegerField()),
                ('course_id', models.PositiveIntegerField()),
                ('question_num', models.PositiveSmallIntegerField()),
                ('title', models.CharField(max_length=31, default='')),
                ('description', models.TextField(default='')),
                ('json_choices', models.CharField(max_length=1055, default='{}')),
                ('json_answers', models.CharField(max_length=127, default='{}')),
            ],
            options={
                'db_table': 'at_multiple_choice_questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MultipleChoiceSubmission',
            fields=[
                ('submission_id', models.AutoField(serialize=False, primary_key=True, max_length=11)),
                ('student_id', models.BigIntegerField()),
                ('assignment_id', models.PositiveIntegerField()),
                ('exam_id', models.PositiveIntegerField(default=0)),
                ('course_id', models.PositiveIntegerField()),
                ('question_num', models.PositiveSmallIntegerField(default=0)),
                ('json_answers', models.CharField(max_length=127, default='{}')),
                ('marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateTimeField(auto_now=True, auto_now_add=True, null=True)),
                ('is_marked', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'at_multiple_choice_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('policy_id', models.AutoField(serialize=False, primary_key=True, max_length=11)),
                ('course_id', models.PositiveIntegerField()),
                ('url', models.URLField(default='')),
            ],
            options={
                'db_table': 'at_policys',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('quiz_id', models.AutoField(serialize=False, primary_key=True, max_length=11)),
                ('course_id', models.PositiveIntegerField()),
                ('order_num', models.PositiveSmallIntegerField(default=0)),
                ('type', models.PositiveSmallIntegerField()),
                ('due_date', models.DateField(null=True)),
            ],
            options={
                'db_table': 'at_quizzes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuizSubmission',
            fields=[
                ('submission_id', models.AutoField(serialize=False, primary_key=True, max_length=11)),
                ('quiz_id', models.PositiveIntegerField()),
                ('student_id', models.BigIntegerField()),
                ('course_id', models.PositiveIntegerField()),
                ('order_num', models.PositiveSmallIntegerField(default=0)),
                ('type', models.PositiveSmallIntegerField()),
                ('marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateField(null=True)),
                ('is_marked', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'at_quiz_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResponseQuestion',
            fields=[
                ('question_id', models.AutoField(serialize=False, primary_key=True, max_length=11)),
                ('assignment_id', models.PositiveIntegerField()),
                ('course_id', models.PositiveIntegerField()),
                ('question_num', models.PositiveSmallIntegerField()),
                ('title', models.CharField(max_length=31, default='')),
                ('description', models.TextField(default='')),
                ('answer', models.TextField(default='')),
            ],
            options={
                'db_table': 'at_response_questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResponseSubmission',
            fields=[
                ('submission_id', models.AutoField(serialize=False, primary_key=True, max_length=11)),
                ('student_id', models.BigIntegerField()),
                ('assignment_id', models.PositiveIntegerField()),
                ('course_id', models.PositiveIntegerField()),
                ('question_num', models.PositiveSmallIntegerField(default=0)),
                ('answer', models.TextField(default='')),
                ('marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateTimeField(auto_now=True, auto_now_add=True, null=True)),
                ('is_marked', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'at_response_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True)),
                ('courses', models.ManyToManyField(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_students',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Syllabus',
            fields=[
                ('syllabus_id', models.AutoField(serialize=False, primary_key=True)),
                ('file', models.FileField(upload_to='uploads', null=True)),
                ('url', models.URLField(default='')),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_syllabus',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True)),
                ('courses', models.ManyToManyField(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_teachers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TrueFalseQuestion',
            fields=[
                ('question_id', models.AutoField(serialize=False, primary_key=True, max_length=11)),
                ('assignment_id', models.PositiveIntegerField(default=0)),
                ('quiz_id', models.PositiveIntegerField(default=0)),
                ('course_id', models.PositiveIntegerField()),
                ('question_num', models.PositiveSmallIntegerField()),
                ('title', models.CharField(max_length=31, default='')),
                ('description', models.TextField(default='')),
                ('true_choice', models.CharField(max_length=127, null=True)),
                ('false_choice', models.CharField(max_length=127, null=True)),
                ('answer', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'at_true_false_questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TrueFalseSubmission',
            fields=[
                ('submission_id', models.AutoField(serialize=False, primary_key=True, max_length=11)),
                ('student_id', models.BigIntegerField()),
                ('assignment_id', models.PositiveIntegerField(default=0)),
                ('quiz_id', models.PositiveIntegerField(default=0)),
                ('course_id', models.PositiveIntegerField()),
                ('question_num', models.PositiveSmallIntegerField(default=0)),
                ('answer', models.BooleanField(default=False)),
                ('marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateTimeField(auto_now=True, auto_now_add=True, null=True)),
                ('is_marked', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'at_true_false_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('week_id', models.AutoField(serialize=False, primary_key=True, max_length=11)),
                ('course_id', models.PositiveIntegerField()),
                ('week_num', models.PositiveSmallIntegerField(max_length=7)),
                ('title', models.CharField(max_length=31)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'at_weeks',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='announcement',
            name='course',
            field=models.ForeignKey(to='registrar.Course'),
            preserve_default=True,
        ),
    ]
