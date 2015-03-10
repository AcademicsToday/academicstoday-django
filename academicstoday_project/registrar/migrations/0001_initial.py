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
                ('announcement_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=31)),
                ('body', models.TextField()),
                ('post_date', models.DateField(auto_now_add=True, auto_now=True, null=True)),
            ],
            options={
                'db_table': 'at_announcements',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('assignment_id', models.AutoField(primary_key=True, serialize=False)),
                ('assignment_num', models.PositiveSmallIntegerField(default=0)),
                ('title', models.CharField(max_length=31, null=True)),
                ('description', models.TextField(null=True)),
                ('start_date', models.DateField(null=True)),
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
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=31)),
                ('comment', models.TextField()),
                ('marks', models.PositiveSmallIntegerField(default=0)),
                ('post_date', models.DateField(auto_now_add=True, auto_now=True, null=True)),
                ('assignment', models.ForeignKey(to='registrar.Assignment', null=True)),
            ],
            options={
                'db_table': 'at_assignment_reviews',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AssignmentSubmission',
            fields=[
                ('submission_id', models.AutoField(primary_key=True, serialize=False)),
                ('assignment_num', models.PositiveSmallIntegerField(default=0)),
                ('type', models.PositiveSmallIntegerField()),
                ('marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateField(null=True)),
                ('is_marked', models.BooleanField(default=False)),
                ('assignment', models.ForeignKey(to='registrar.Assignment')),
            ],
            options={
                'db_table': 'at_assignment_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
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
                ('question_id', models.AutoField(max_length=11, primary_key=True, serialize=False)),
                ('question_num', models.PositiveSmallIntegerField()),
                ('title', models.CharField(max_length=31, default='')),
                ('description', models.TextField(default='')),
                ('assignment', models.ForeignKey(to='registrar.Assignment')),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_essay_questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EssaySubmission',
            fields=[
                ('submission_id', models.AutoField(max_length=11, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='uploads')),
                ('submission_date', models.DateTimeField(auto_now_add=True, auto_now=True, null=True)),
                ('is_marked', models.BooleanField(default=False)),
                ('assignment', models.ForeignKey(to='registrar.Assignment')),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_essay_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('exam_id', models.AutoField(primary_key=True, serialize=False)),
                ('exam_num', models.PositiveSmallIntegerField(default=0)),
                ('type', models.PositiveSmallIntegerField()),
                ('start_date', models.DateField(null=True)),
                ('due_date', models.DateField(null=True)),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_exams',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExamSubmission',
            fields=[
                ('submission_id', models.AutoField(primary_key=True, serialize=False)),
                ('exam_num', models.PositiveSmallIntegerField(default=0)),
                ('type', models.PositiveSmallIntegerField()),
                ('marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateField(null=True)),
                ('is_marked', models.BooleanField(default=False)),
                ('course', models.ForeignKey(to='registrar.Course')),
                ('exam', models.ForeignKey(to='registrar.Exam')),
            ],
            options={
                'db_table': 'at_exam_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('lecture_id', models.AutoField(primary_key=True, serialize=False)),
                ('lecture_num', models.PositiveSmallIntegerField(max_length=7, default=0)),
                ('week_num', models.PositiveSmallIntegerField(max_length=7)),
                ('title', models.CharField(max_length=31, null=True, default='')),
                ('description', models.TextField(null=True, default='')),
                ('youtube_url', models.URLField(null=True, default='')),
                ('vimeo_url', models.URLField(null=True, default='')),
                ('bliptv_url', models.URLField(null=True, default='')),
                ('preferred_service', models.CharField(max_length=31)),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_lectures',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('question_num', models.PositiveSmallIntegerField()),
                ('title', models.CharField(max_length=31, default='')),
                ('description', models.TextField(default='')),
                ('a', models.CharField(max_length=255, null=True)),
                ('a_is_correct', models.BooleanField(default=False)),
                ('b', models.CharField(max_length=255, null=True)),
                ('b_is_correct', models.BooleanField(default=False)),
                ('c', models.CharField(max_length=255, null=True)),
                ('c_is_correct', models.BooleanField(default=False)),
                ('d', models.CharField(max_length=255, null=True)),
                ('d_is_correct', models.BooleanField(default=False)),
                ('e', models.CharField(max_length=255, null=True)),
                ('e_is_correct', models.BooleanField(default=False)),
                ('f', models.CharField(max_length=255, null=True)),
                ('f_is_correct', models.BooleanField(default=False)),
                ('assignment', models.ForeignKey(to='registrar.Assignment', null=True)),
                ('course', models.ForeignKey(to='registrar.Course')),
                ('exam', models.ForeignKey(to='registrar.Exam', null=True)),
            ],
            options={
                'db_table': 'at_multiple_choice_questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MultipleChoiceSubmission',
            fields=[
                ('submission_id', models.AutoField(max_length=11, primary_key=True, serialize=False)),
                ('question_num', models.PositiveSmallIntegerField(default=0)),
                ('json_answers', models.CharField(max_length=127, default='{}')),
                ('marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateTimeField(auto_now_add=True, auto_now=True, null=True)),
                ('is_marked', models.BooleanField(default=False)),
                ('assignment', models.ForeignKey(to='registrar.Assignment', null=True)),
                ('course', models.ForeignKey(to='registrar.Course')),
                ('exam', models.ForeignKey(to='registrar.Exam', null=True)),
            ],
            options={
                'db_table': 'at_multiple_choice_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('policy_id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='uploads', null=True)),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_policys',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('quiz_id', models.AutoField(primary_key=True, serialize=False)),
                ('quiz_num', models.PositiveSmallIntegerField(default=0)),
                ('title', models.CharField(max_length=31, null=True)),
                ('description', models.TextField(null=True)),
                ('start_date', models.DateField(null=True)),
                ('due_date', models.DateField(null=True)),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_quizzes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuizSubmission',
            fields=[
                ('submission_id', models.AutoField(primary_key=True, serialize=False)),
                ('quiz_id', models.PositiveIntegerField()),
                ('quiz_num', models.PositiveSmallIntegerField(default=0)),
                ('type', models.PositiveSmallIntegerField()),
                ('marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateField(null=True)),
                ('is_marked', models.BooleanField(default=False)),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_quiz_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResponseQuestion',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('question_num', models.PositiveSmallIntegerField()),
                ('title', models.CharField(max_length=31, default='')),
                ('description', models.TextField(default='')),
                ('answer', models.TextField(default='')),
                ('assignment', models.ForeignKey(to='registrar.Assignment', null=True)),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_response_questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResponseSubmission',
            fields=[
                ('submission_id', models.AutoField(primary_key=True, serialize=False)),
                ('question_num', models.PositiveSmallIntegerField(default=0)),
                ('answer', models.TextField(default='')),
                ('marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateTimeField(auto_now_add=True, auto_now=True, null=True)),
                ('is_marked', models.BooleanField(default=False)),
                ('assignment', models.ForeignKey(to='registrar.Assignment', null=True)),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_response_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, primary_key=True, serialize=False)),
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
                ('syllabus_id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='uploads', null=True)),
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
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, primary_key=True, serialize=False)),
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
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('question_num', models.PositiveSmallIntegerField()),
                ('title', models.CharField(max_length=31, default='')),
                ('description', models.TextField(default='')),
                ('true_choice', models.CharField(max_length=127, null=True)),
                ('false_choice', models.CharField(max_length=127, null=True)),
                ('answer', models.BooleanField(default=False)),
                ('assignment', models.ForeignKey(to='registrar.Assignment', null=True)),
                ('course', models.ForeignKey(to='registrar.Course')),
                ('quiz', models.ForeignKey(to='registrar.Quiz', null=True)),
            ],
            options={
                'db_table': 'at_true_false_questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TrueFalseSubmission',
            fields=[
                ('submission_id', models.AutoField(primary_key=True, serialize=False)),
                ('question_num', models.PositiveSmallIntegerField(default=0)),
                ('answer', models.BooleanField(default=False)),
                ('marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateTimeField(auto_now_add=True, auto_now=True, null=True)),
                ('is_marked', models.BooleanField(default=False)),
                ('assignment', models.ForeignKey(to='registrar.Assignment', null=True)),
                ('course', models.ForeignKey(to='registrar.Course')),
                ('quiz', models.ForeignKey(to='registrar.Quiz', null=True)),
                ('student', models.ForeignKey(to='registrar.Student')),
            ],
            options={
                'db_table': 'at_true_false_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('week_id', models.AutoField(max_length=11, primary_key=True, serialize=False)),
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
            model_name='responsesubmission',
            name='student',
            field=models.ForeignKey(to='registrar.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quizsubmission',
            name='student',
            field=models.ForeignKey(to='registrar.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicesubmission',
            name='student',
            field=models.ForeignKey(to='registrar.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='examsubmission',
            name='student',
            field=models.ForeignKey(to='registrar.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='essaysubmission',
            name='student',
            field=models.ForeignKey(to='registrar.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='course',
            field=models.ForeignKey(to='registrar.Course'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='student',
            field=models.ForeignKey(to='registrar.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignmentreview',
            name='course',
            field=models.ForeignKey(to='registrar.Course'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignmentreview',
            name='student',
            field=models.ForeignKey(to='registrar.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(to='registrar.Course'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='announcement',
            name='course',
            field=models.ForeignKey(to='registrar.Course'),
            preserve_default=True,
        ),
    ]
