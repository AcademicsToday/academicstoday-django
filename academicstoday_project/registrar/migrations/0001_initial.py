# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('announcement_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=31)),
                ('body', models.TextField()),
                ('post_date', models.DateField(null=True, auto_now=True, auto_now_add=True)),
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
                ('title', models.CharField(null=True, max_length=31)),
                ('description', models.TextField(null=True)),
                ('start_date', models.DateField(null=True)),
                ('due_date', models.DateField(null=True)),
                ('worth', models.PositiveSmallIntegerField(choices=[(0, '0 %'), (10, '10 %'), (15, '15 %'), (20, '20 %'), (25, '25 %'), (30, '30 %'), (35, '35 %'), (40, '40 %'), (45, '45 %'), (50, '50 %'), (55, '55 %'), (60, '60 %'), (65, '65 %'), (70, '70 %'), (75, '75 %'), (80, '80 %'), (85, '85 %'), (90, '90 %'), (95, '95 %'), (100, '100 %')], default=0)),
            ],
            options={
                'db_table': 'at_assignments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AssignmentSubmission',
            fields=[
                ('submission_id', models.AutoField(primary_key=True, serialize=False)),
                ('percent', models.FloatField(default=0)),
                ('earned_marks', models.FloatField(default=0)),
                ('total_marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateTimeField(null=True, auto_now=True)),
                ('is_finished', models.BooleanField(default=False)),
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
                ('category', models.CharField(choices=[('Liberal Arts', 'Liberal Arts')], max_length=127)),
                ('description', models.TextField(null=True)),
                ('start_date', models.DateField(null=True)),
                ('finish_date', models.DateField(null=True)),
                ('is_official', models.BooleanField(default=False)),
                ('status', models.PositiveSmallIntegerField(default=0)),
                ('file', models.FileField(null=True, upload_to='uploads')),
            ],
            options={
                'db_table': 'at_courses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseDiscussionPost',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=127)),
                ('text', models.TextField(null=True, blank=True)),
                ('date', models.DateTimeField(null=True, auto_now=True, auto_now_add=True)),
            ],
            options={
                'db_table': 'at_course_discussion_posts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseDiscussionThread',
            fields=[
                ('thread_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=127)),
                ('text', models.TextField(null=True, blank=True)),
                ('date', models.DateTimeField(null=True, auto_now=True, auto_now_add=True)),
                ('course', models.ForeignKey(to='registrar.Course')),
                ('posts', models.ManyToManyField(to='registrar.CourseDiscussionPost')),
            ],
            options={
                'db_table': 'at_course_discussion_threads',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseFinalMark',
            fields=[
                ('credit_id', models.AutoField(primary_key=True, serialize=False)),
                ('percent', models.FloatField(default=0)),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_course_final_marks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseSetting',
            fields=[
                ('settings_id', models.AutoField(primary_key=True, serialize=False)),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_course_settings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseSubmission',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.PositiveSmallIntegerField(default=2)),
                ('from_submitter', models.TextField(null=True)),
                ('from_reviewer', models.TextField(null=True)),
                ('review_date', models.DateField(null=True, auto_now=True)),
                ('submission_date', models.DateField(null=True, auto_now_add=True)),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_course_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EssayQuestion',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('question_num', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('title', models.CharField(default='', max_length=31)),
                ('description', models.TextField(default='')),
                ('marks', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('assignment', models.ForeignKey(null=True, to='registrar.Assignment')),
            ],
            options={
                'db_table': 'at_essay_questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EssaySubmission',
            fields=[
                ('submission_id', models.AutoField(primary_key=True, serialize=False, max_length=11)),
                ('file', models.FileField(upload_to='uploads')),
                ('submission_date', models.DateTimeField(null=True, auto_now=True, auto_now_add=True)),
                ('marks', models.FloatField(default=0)),
                ('question', models.ForeignKey(to='registrar.EssayQuestion')),
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
                ('title', models.CharField(null=True, max_length=31)),
                ('description', models.TextField(null=True)),
                ('start_date', models.DateField(null=True)),
                ('due_date', models.DateField(null=True)),
                ('worth', models.PositiveSmallIntegerField(choices=[(0, '0 %'), (10, '10 %'), (15, '15 %'), (20, '20 %'), (25, '25 %'), (30, '30 %'), (35, '35 %'), (40, '40 %'), (45, '45 %'), (50, '50 %'), (55, '55 %'), (60, '60 %'), (65, '65 %'), (70, '70 %'), (75, '75 %'), (80, '80 %'), (85, '85 %'), (90, '90 %'), (95, '95 %'), (100, '100 %')], default=0)),
                ('is_final', models.BooleanField(default=False)),
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
                ('percent', models.FloatField(default=0)),
                ('earned_marks', models.FloatField(default=0)),
                ('total_marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateField(null=True)),
                ('is_finished', models.BooleanField(default=False)),
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
                ('lecture_num', models.PositiveSmallIntegerField(default=0, max_length=7)),
                ('week_num', models.PositiveSmallIntegerField(max_length=7)),
                ('title', models.CharField(null=True, default='', max_length=31)),
                ('description', models.TextField(null=True, default='')),
                ('youtube_url', models.URLField(null=True, blank=True)),
                ('vimeo_url', models.URLField(null=True, blank=True)),
                ('bliptv_url', models.URLField(null=True, blank=True)),
                ('preferred_service', models.CharField(choices=[('1', 'YouTube'), ('2', 'Vimeo')], default='1', max_length=1)),
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
                ('title', models.CharField(default='', blank=True, max_length=31)),
                ('description', models.TextField(default='')),
                ('a', models.CharField(null=True, max_length=255)),
                ('a_is_correct', models.BooleanField(default=False)),
                ('b', models.CharField(null=True, max_length=255)),
                ('b_is_correct', models.BooleanField(default=False)),
                ('c', models.CharField(null=True, blank=True, max_length=255)),
                ('c_is_correct', models.BooleanField(default=False)),
                ('d', models.CharField(null=True, blank=True, max_length=255)),
                ('d_is_correct', models.BooleanField(default=False)),
                ('e', models.CharField(null=True, blank=True, max_length=255)),
                ('e_is_correct', models.BooleanField(default=False)),
                ('f', models.CharField(null=True, blank=True, max_length=255)),
                ('f_is_correct', models.BooleanField(default=False)),
                ('marks', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('assignment', models.ForeignKey(null=True, to='registrar.Assignment')),
                ('exam', models.ForeignKey(null=True, to='registrar.Exam')),
            ],
            options={
                'db_table': 'at_multiple_choice_questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MultipleChoiceSubmission',
            fields=[
                ('submission_id', models.AutoField(primary_key=True, serialize=False, max_length=11)),
                ('a', models.BooleanField(default=False)),
                ('b', models.BooleanField(default=False)),
                ('c', models.BooleanField(default=False)),
                ('d', models.BooleanField(default=False)),
                ('e', models.BooleanField(default=False)),
                ('f', models.BooleanField(default=False)),
                ('marks', models.FloatField(default=0)),
                ('submission_date', models.DateTimeField(null=True, auto_now=True, auto_now_add=True)),
                ('question', models.ForeignKey(to='registrar.MultipleChoiceQuestion')),
            ],
            options={
                'db_table': 'at_multiple_choice_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PeerReview',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False, max_length=11)),
                ('marks', models.PositiveSmallIntegerField(choices=[(0, '0 Star'), (1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], default=0)),
                ('text', models.TextField(null=True, blank=True)),
                ('date', models.DateTimeField(null=True, auto_now=True, auto_now_add=True)),
            ],
            options={
                'db_table': 'at_peer_reviews',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('policy_id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(null=True, upload_to='uploads')),
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
                ('title', models.CharField(null=True, max_length=31)),
                ('description', models.TextField(null=True)),
                ('start_date', models.DateField(null=True)),
                ('due_date', models.DateField(null=True)),
                ('worth', models.PositiveSmallIntegerField(choices=[(0, '0 %'), (10, '10 %'), (15, '15 %'), (20, '20 %'), (25, '25 %'), (30, '30 %'), (35, '35 %'), (40, '40 %'), (45, '45 %'), (50, '50 %'), (55, '55 %'), (60, '60 %'), (65, '65 %'), (70, '70 %'), (75, '75 %'), (80, '80 %'), (85, '85 %'), (90, '90 %'), (95, '95 %'), (100, '100 %')], default=0)),
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
                ('percent', models.FloatField(default=0)),
                ('earned_marks', models.FloatField(default=0)),
                ('total_marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateField(null=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('quiz', models.ForeignKey(to='registrar.Quiz')),
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
                ('title', models.CharField(default='', max_length=31)),
                ('description', models.TextField(default='')),
                ('answer', models.TextField(default='')),
                ('marks', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('assignment', models.ForeignKey(null=True, to='registrar.Assignment')),
                ('exam', models.ForeignKey(null=True, to='registrar.Exam')),
                ('quiz', models.ForeignKey(null=True, to='registrar.Quiz')),
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
                ('answer', models.TextField(default='')),
                ('marks', models.FloatField(default=0)),
                ('submission_date', models.DateTimeField(null=True, auto_now=True, auto_now_add=True)),
                ('question', models.ForeignKey(to='registrar.ResponseQuestion')),
                ('reviews', models.ManyToManyField(to='registrar.PeerReview')),
            ],
            options={
                'db_table': 'at_response_submissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('courses', models.ManyToManyField(to='registrar.Course')),
                ('transcript', models.ManyToManyField(to='registrar.CourseFinalMark')),
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
                ('file', models.FileField(null=True, upload_to='uploads')),
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
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
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
                ('title', models.CharField(default='', max_length=31)),
                ('description', models.TextField(default='')),
                ('true_choice', models.CharField(null=True, max_length=127)),
                ('false_choice', models.CharField(null=True, max_length=127)),
                ('answer', models.BooleanField(default=False)),
                ('marks', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('assignment', models.ForeignKey(null=True, to='registrar.Assignment')),
                ('exam', models.ForeignKey(null=True, to='registrar.Exam')),
                ('quiz', models.ForeignKey(null=True, to='registrar.Quiz')),
            ],
            options={
                'db_table': 'at_true_false_questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TrueFalseSubmission',
            fields=[
                ('submission_id', models.AutoField(primary_key=True, serialize=False, max_length=11)),
                ('answer', models.BooleanField(default=False)),
                ('submission_date', models.DateTimeField(null=True, auto_now=True, auto_now_add=True)),
                ('marks', models.FloatField(default=0)),
                ('question', models.ForeignKey(to='registrar.TrueFalseQuestion')),
                ('student', models.ForeignKey(to='registrar.Student')),
            ],
            options={
                'db_table': 'at_true_false_submissions',
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
            model_name='peerreview',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicesubmission',
            name='student',
            field=models.ForeignKey(to='registrar.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='quiz',
            field=models.ForeignKey(null=True, to='registrar.Quiz'),
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
            name='reviews',
            field=models.ManyToManyField(to='registrar.PeerReview'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='essaysubmission',
            name='student',
            field=models.ForeignKey(to='registrar.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='essayquestion',
            name='exam',
            field=models.ForeignKey(null=True, to='registrar.Exam'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='essayquestion',
            name='quiz',
            field=models.ForeignKey(null=True, to='registrar.Quiz'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coursediscussionthread',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coursediscussionpost',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
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
