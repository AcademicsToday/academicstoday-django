# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('announcement_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=31)),
                ('body', models.TextField()),
                ('post_date', models.DateField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'at_announcements',
            },
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('assignment_id', models.AutoField(serialize=False, primary_key=True)),
                ('assignment_num', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('title', models.CharField(max_length=31, null=True)),
                ('description', models.TextField(null=True)),
                ('start_date', models.DateField(null=True)),
                ('due_date', models.DateField(null=True)),
                ('worth', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], choices=[(0, '0 %'), (10, '10 %'), (15, '15 %'), (20, '20 %'), (25, '25 %'), (30, '30 %'), (35, '35 %'), (40, '40 %'), (45, '45 %'), (50, '50 %'), (55, '55 %'), (60, '60 %'), (65, '65 %'), (70, '70 %'), (75, '75 %'), (80, '80 %'), (85, '85 %'), (90, '90 %'), (95, '95 %'), (100, '100 %')])),
            ],
            options={
                'db_table': 'at_assignments',
            },
        ),
        migrations.CreateModel(
            name='AssignmentSubmission',
            fields=[
                ('submission_id', models.AutoField(serialize=False, primary_key=True)),
                ('percent', models.FloatField(default=0)),
                ('earned_marks', models.FloatField(default=0)),
                ('total_marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateTimeField(auto_now=True, null=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('assignment', models.ForeignKey(to='registrar.Assignment')),
                ('student', models.ForeignKey(to='account.Student')),
            ],
            options={
                'db_table': 'at_assignment_submissions',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=127)),
                ('sub_title', models.CharField(max_length=127)),
                ('category', models.CharField(default='General Education', max_length=127, choices=[('Aeronautics & Astronautics', 'Aeronautics & Astronautics'), ('Anesthesia', 'Anesthesia'), ('Anthropology', 'Anthropology'), ('Applied Physics', 'Applied Physics'), ('Art or Art History', 'Art & Art History'), ('Astrophysics', 'Astrophysics'), ('Biochemistry', 'Biochemistry'), ('Bioengineering', 'Bioengineering'), ('Biology', 'Biology'), ('Business', 'Business'), ('Cardiothoracic Surgery', 'Cardiothoracic Surgery'), ('Chemical and Systems Biology', 'Chemical and Systems Biology'), ('Chemical Engineering', 'Chemical Engineering'), ('Chemistry', 'Chemistry'), ('Civil and Environmental Engineering', 'Civil and Environmental Engineering'), ('Classics', 'Classics'), ('Communication', 'Communication'), ('Comparative Literature', 'Comparative Literature'), ('Comparative Medicine', 'Comparative Medicine'), ('Computer Science', 'Computer Science'), ('Dermatology', 'Dermatology'), ('Developmental Biology', 'Developmental Biology'), ('East Asian Languages and Cultures', 'East Asian Languages and Cultures'), ('Economics', 'Economics'), ('Education', 'Education'), ('Electrical Engineering', 'Electrical Engineering'), ('English', 'English'), ('French', 'French'), ('Genetics', 'Genetics'), ('General Eduction', 'General Education'), ('Geological and Environmental Sciences', 'Geological and Environmental Sciences'), ('Geophysics', 'Geophysics'), ('Health', 'Health'), ('History', 'History'), ('Latin American Cultures', 'Latin American Cultures'), ('Law School', 'Law School'), ('Linguistics', 'Linguistics'), ('Management', 'Management'), ('Materials Science', 'Materials Science'), ('Mathematics', 'Mathematics'), ('Mechanical Engineering', 'Mechanical Engineering'), ('Medicine', 'Medicine'), ('Microbiology and Immunology', 'Microbiology and Immunology'), ('Molecular and Cellular Physiology', 'Molecular and Cellular Physiology'), ('Music', 'Music'), ('Neurobiology', 'Neurobiology'), ('Neurology', 'Neurology'), ('Neurosurgery', 'Neurosurgery'), ('Obstetrics and Gynecology', 'Obstetrics and Gynecology'), ('Ophthalmology', 'Ophthalmology'), ('Orthopaedic Surgery', 'Orthopaedic Surgery'), ('Other', 'Other'), ('Otolaryngology', 'Otolaryngology'), ('Pathology', 'Pathology'), ('Pediatrics', 'Pediatrics'), ('Philosophy', 'Philosophy'), ('Physics', 'Physics'), ('Political Science', 'Political Science'), ('Psychiatry', 'Psychiatry'), ('Psychology', 'Psychology'), ('Radiation Oncology', 'Radiation Oncology'), ('Radiology', 'Radiology'), ('Religious Studies', 'Religious Studies'), ('Slavic Languages and Literature', 'Slavic Languages and Literature'), ('Sociology', 'Sociology'), ('Statistics', 'Statistics'), ('Surgery', 'Surgery'), ('Theater and Performance Studies', 'Theater and Performance Studies'), ('Urology', 'Urology')])),
                ('description', models.TextField(null=True)),
                ('start_date', models.DateField(null=True)),
                ('finish_date', models.DateField(null=True)),
                ('is_official', models.BooleanField(default=False)),
                ('status', models.PositiveSmallIntegerField(default=0)),
                ('image', models.ImageField(upload_to='uploads', null=True)),
                ('students', models.ManyToManyField(to='account.Student')),
                ('teacher', models.ForeignKey(to='account.Teacher')),
            ],
            options={
                'db_table': 'at_courses',
            },
        ),
        migrations.CreateModel(
            name='CourseDiscussionPost',
            fields=[
                ('post_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=127)),
                ('text', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'at_course_discussion_posts',
            },
        ),
        migrations.CreateModel(
            name='CourseDiscussionThread',
            fields=[
                ('thread_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=127)),
                ('text', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('course', models.ForeignKey(to='registrar.Course')),
                ('posts', models.ManyToManyField(to='registrar.CourseDiscussionPost')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'at_course_discussion_threads',
            },
        ),
        migrations.CreateModel(
            name='CourseFinalMark',
            fields=[
                ('credit_id', models.AutoField(serialize=False, primary_key=True)),
                ('percent', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('is_public', models.BooleanField(default=False)),
                ('course', models.ForeignKey(to='registrar.Course')),
                ('student', models.ForeignKey(to='account.Student')),
            ],
            options={
                'db_table': 'at_course_final_marks',
            },
        ),
        migrations.CreateModel(
            name='CourseSetting',
            fields=[
                ('settings_id', models.AutoField(serialize=False, primary_key=True)),
                ('final_exam_percent', models.FloatField(default=50, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('course_percent', models.FloatField(default=50, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_course_settings',
            },
        ),
        migrations.CreateModel(
            name='CourseSubmission',
            fields=[
                ('review_id', models.AutoField(serialize=False, primary_key=True)),
                ('status', models.PositiveSmallIntegerField(default=2)),
                ('from_submitter', models.TextField(null=True)),
                ('from_reviewer', models.TextField(null=True)),
                ('review_date', models.DateField(auto_now=True, null=True)),
                ('submission_date', models.DateField(auto_now=True, null=True)),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_course_submissions',
            },
        ),
        migrations.CreateModel(
            name='EssayQuestion',
            fields=[
                ('question_id', models.AutoField(serialize=False, primary_key=True)),
                ('question_num', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('title', models.CharField(default='', max_length=31)),
                ('description', models.TextField(default='')),
                ('marks', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('assignment', models.ForeignKey(to='registrar.Assignment', null=True)),
            ],
            options={
                'db_table': 'at_essay_questions',
            },
        ),
        migrations.CreateModel(
            name='EssaySubmission',
            fields=[
                ('submission_id', models.AutoField(serialize=False, primary_key=True)),
                ('file', models.FileField(upload_to='uploads')),
                ('submission_date', models.DateTimeField(auto_now=True, null=True)),
                ('marks', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('question', models.ForeignKey(to='registrar.EssayQuestion')),
            ],
            options={
                'db_table': 'at_essay_submissions',
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('exam_id', models.AutoField(serialize=False, primary_key=True)),
                ('exam_num', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('title', models.CharField(max_length=31, null=True)),
                ('description', models.TextField(null=True)),
                ('start_date', models.DateField(null=True)),
                ('due_date', models.DateField(null=True)),
                ('worth', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], choices=[(0, '0 %'), (10, '10 %'), (15, '15 %'), (20, '20 %'), (25, '25 %'), (30, '30 %'), (35, '35 %'), (40, '40 %'), (45, '45 %'), (50, '50 %'), (55, '55 %'), (60, '60 %'), (65, '65 %'), (70, '70 %'), (75, '75 %'), (80, '80 %'), (85, '85 %'), (90, '90 %'), (95, '95 %'), (100, '100 %')])),
                ('is_final', models.BooleanField(default=False)),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_exams',
            },
        ),
        migrations.CreateModel(
            name='ExamSubmission',
            fields=[
                ('submission_id', models.AutoField(serialize=False, primary_key=True)),
                ('percent', models.FloatField(default=0)),
                ('earned_marks', models.FloatField(default=0)),
                ('total_marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateField(auto_now=True, null=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('exam', models.ForeignKey(to='registrar.Exam')),
                ('student', models.ForeignKey(to='account.Student')),
            ],
            options={
                'db_table': 'at_exam_submissions',
            },
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('upload_id', models.AutoField(serialize=False, primary_key=True)),
                ('type', models.PositiveSmallIntegerField(default=0)),
                ('title', models.CharField(max_length=127, null=True)),
                ('description', models.TextField(null=True)),
                ('upload_date', models.DateField(auto_now=True, null=True)),
                ('file', models.FileField(upload_to='uploads', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'at_file_uploads',
            },
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('lecture_id', models.AutoField(serialize=False, primary_key=True)),
                ('lecture_num', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('week_num', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('title', models.CharField(default='', max_length=63, null=True)),
                ('description', models.TextField(default='', null=True)),
                ('youtube_url', models.URLField(blank=True, null=True)),
                ('vimeo_url', models.URLField(blank=True, null=True)),
                ('bliptv_url', models.URLField(blank=True, null=True)),
                ('preferred_service', models.CharField(default='1', max_length=1, choices=[('1', 'YouTube'), ('2', 'Vimeo')])),
                ('course', models.ForeignKey(to='registrar.Course')),
                ('notes', models.ManyToManyField(to='registrar.FileUpload')),
            ],
            options={
                'db_table': 'at_lectures',
            },
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('question_id', models.AutoField(serialize=False, primary_key=True)),
                ('question_num', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('title', models.CharField(default='', blank=True, max_length=31)),
                ('description', models.TextField(default='')),
                ('a', models.CharField(max_length=255, null=True)),
                ('a_is_correct', models.BooleanField(default=False)),
                ('b', models.CharField(max_length=255, null=True)),
                ('b_is_correct', models.BooleanField(default=False)),
                ('c', models.CharField(blank=True, max_length=255, null=True)),
                ('c_is_correct', models.BooleanField(default=False)),
                ('d', models.CharField(blank=True, max_length=255, null=True)),
                ('d_is_correct', models.BooleanField(default=False)),
                ('e', models.CharField(blank=True, max_length=255, null=True)),
                ('e_is_correct', models.BooleanField(default=False)),
                ('f', models.CharField(blank=True, max_length=255, null=True)),
                ('f_is_correct', models.BooleanField(default=False)),
                ('marks', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('assignment', models.ForeignKey(to='registrar.Assignment', null=True)),
                ('exam', models.ForeignKey(to='registrar.Exam', null=True)),
            ],
            options={
                'db_table': 'at_multiple_choice_questions',
            },
        ),
        migrations.CreateModel(
            name='MultipleChoiceSubmission',
            fields=[
                ('submission_id', models.AutoField(serialize=False, primary_key=True)),
                ('a', models.BooleanField(default=False)),
                ('b', models.BooleanField(default=False)),
                ('c', models.BooleanField(default=False)),
                ('d', models.BooleanField(default=False)),
                ('e', models.BooleanField(default=False)),
                ('f', models.BooleanField(default=False)),
                ('marks', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('submission_date', models.DateTimeField(auto_now=True, null=True)),
                ('question', models.ForeignKey(to='registrar.MultipleChoiceQuestion')),
                ('student', models.ForeignKey(to='account.Student')),
            ],
            options={
                'db_table': 'at_multiple_choice_submissions',
            },
        ),
        migrations.CreateModel(
            name='PeerReview',
            fields=[
                ('review_id', models.AutoField(serialize=False, max_length=11, primary_key=True)),
                ('marks', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], choices=[(0, '0 Star'), (1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])),
                ('text', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'at_peer_reviews',
            },
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('policy_id', models.AutoField(serialize=False, primary_key=True)),
                ('file', models.FileField(upload_to='uploads', null=True)),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_policys',
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('quiz_id', models.AutoField(serialize=False, primary_key=True)),
                ('quiz_num', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('title', models.CharField(max_length=31, null=True)),
                ('description', models.TextField(null=True)),
                ('start_date', models.DateField(null=True)),
                ('due_date', models.DateField(null=True)),
                ('worth', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], choices=[(0, '0 %'), (10, '10 %'), (15, '15 %'), (20, '20 %'), (25, '25 %'), (30, '30 %'), (35, '35 %'), (40, '40 %'), (45, '45 %'), (50, '50 %'), (55, '55 %'), (60, '60 %'), (65, '65 %'), (70, '70 %'), (75, '75 %'), (80, '80 %'), (85, '85 %'), (90, '90 %'), (95, '95 %'), (100, '100 %')])),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_quizzes',
            },
        ),
        migrations.CreateModel(
            name='QuizSubmission',
            fields=[
                ('submission_id', models.AutoField(serialize=False, primary_key=True)),
                ('percent', models.FloatField(default=0)),
                ('earned_marks', models.FloatField(default=0)),
                ('total_marks', models.PositiveSmallIntegerField(default=0)),
                ('submission_date', models.DateField(auto_now=True, null=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('quiz', models.ForeignKey(to='registrar.Quiz')),
                ('student', models.ForeignKey(to='account.Student')),
            ],
            options={
                'db_table': 'at_quiz_submissions',
            },
        ),
        migrations.CreateModel(
            name='ResponseQuestion',
            fields=[
                ('question_id', models.AutoField(serialize=False, primary_key=True)),
                ('question_num', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('title', models.CharField(default='', max_length=31)),
                ('description', models.TextField(default='')),
                ('answer', models.TextField(default='')),
                ('marks', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('assignment', models.ForeignKey(to='registrar.Assignment', null=True)),
                ('exam', models.ForeignKey(to='registrar.Exam', null=True)),
                ('quiz', models.ForeignKey(to='registrar.Quiz', null=True)),
            ],
            options={
                'db_table': 'at_response_questions',
            },
        ),
        migrations.CreateModel(
            name='ResponseSubmission',
            fields=[
                ('submission_id', models.AutoField(serialize=False, primary_key=True)),
                ('answer', models.TextField(default='')),
                ('marks', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('submission_date', models.DateTimeField(auto_now=True, null=True)),
                ('question', models.ForeignKey(to='registrar.ResponseQuestion')),
                ('reviews', models.ManyToManyField(to='registrar.PeerReview')),
                ('student', models.ForeignKey(to='account.Student')),
            ],
            options={
                'db_table': 'at_response_submissions',
            },
        ),
        migrations.CreateModel(
            name='Syllabus',
            fields=[
                ('syllabus_id', models.AutoField(serialize=False, primary_key=True)),
                ('file', models.FileField(upload_to='uploads', null=True)),
                ('course', models.ForeignKey(to='registrar.Course')),
            ],
            options={
                'db_table': 'at_syllabus',
            },
        ),
        migrations.CreateModel(
            name='TrueFalseQuestion',
            fields=[
                ('question_id', models.AutoField(serialize=False, primary_key=True)),
                ('question_num', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('title', models.CharField(default='', max_length=31)),
                ('description', models.TextField(default='')),
                ('true_choice', models.CharField(max_length=127, null=True)),
                ('false_choice', models.CharField(max_length=127, null=True)),
                ('answer', models.BooleanField(default=False)),
                ('marks', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('assignment', models.ForeignKey(to='registrar.Assignment', null=True)),
                ('exam', models.ForeignKey(to='registrar.Exam', null=True)),
                ('quiz', models.ForeignKey(to='registrar.Quiz', null=True)),
            ],
            options={
                'db_table': 'at_true_false_questions',
            },
        ),
        migrations.CreateModel(
            name='TrueFalseSubmission',
            fields=[
                ('submission_id', models.AutoField(serialize=False, primary_key=True)),
                ('answer', models.BooleanField(default=False)),
                ('submission_date', models.DateTimeField(auto_now=True, null=True)),
                ('marks', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('question', models.ForeignKey(to='registrar.TrueFalseQuestion')),
                ('student', models.ForeignKey(to='account.Student')),
            ],
            options={
                'db_table': 'at_true_false_submissions',
            },
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='quiz',
            field=models.ForeignKey(to='registrar.Quiz', null=True),
        ),
        migrations.AddField(
            model_name='essaysubmission',
            name='reviews',
            field=models.ManyToManyField(to='registrar.PeerReview'),
        ),
        migrations.AddField(
            model_name='essaysubmission',
            name='student',
            field=models.ForeignKey(to='account.Student'),
        ),
        migrations.AddField(
            model_name='essayquestion',
            name='exam',
            field=models.ForeignKey(to='registrar.Exam', null=True),
        ),
        migrations.AddField(
            model_name='essayquestion',
            name='quiz',
            field=models.ForeignKey(to='registrar.Quiz', null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(to='registrar.Course'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='course',
            field=models.ForeignKey(to='registrar.Course'),
        ),
    ]
