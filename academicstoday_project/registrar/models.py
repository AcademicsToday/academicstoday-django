from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

WORTH_PERCENT_CHOICES = (
    (0, '0 %'),
    (10, '10 %'),
    (15, '15 %'),
    (20, '20 %'),
    (25, '25 %'),
    (30, '30 %'),
    (35, '35 %'),
    (40, '40 %'),
    (45, '45 %'),
    (50, '50 %'),
    (55, '55 %'),
    (60, '60 %'),
    (65, '65 %'),
    (70, '70 %'),
    (75, '75 %'),
    (80, '80 %'),
    (85, '85 %'),
    (90, '90 %'),
    (95, '95 %'),
    (100, '100 %'),
)

class Course(models.Model):
    COURSE_CATEGORY_TYPES = (
        ('Liberal Arts', 'Liberal Arts'),
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=127)
    sub_title = models.CharField(max_length=127)
    category = models.CharField(max_length=127, choices=COURSE_CATEGORY_TYPES)
    description = models.TextField(null=True)
    start_date = models.DateField(null=True)
    finish_date = models.DateField(null=True)
    is_official = models.BooleanField(default=False)
    status = models.PositiveSmallIntegerField(default=settings.COURSE_UNAVAILABLE_STATUS)
    file = models.FileField(upload_to='uploads',null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'at_courses'


class CourseSubmission(models.Model):
    review_id = models.AutoField(primary_key=True)
    status = models.PositiveSmallIntegerField(default=settings.COURSE_SUBMITTED_FOR_REVIEW_STATUS)
    from_submitter = models.TextField(null=True)
    from_reviewer = models.TextField(null=True)
    review_date = models.DateField(auto_now=True, null=True)
    submission_date = models.DateField(auto_now_add=True, null=True)
    course = models.ForeignKey(Course)

    def __str__(self):
        return str(self.review_date) + ' ' + str(self.review)

    class Meta:
        db_table = 'at_course_submissions'


class CourseSetting(models.Model):
    settings_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course)
    
    def __str__(self):
        return str(self.settings_id);
    
    class Meta:
        db_table = 'at_course_settings'


class CourseFinalMark(models.Model):
    credit_id = models.AutoField(primary_key=True)
    percent = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    course = models.ForeignKey(Course)
    
    def __str__(self):
        return self.user
    
    class Meta:
        db_table = 'at_course_final_marks'


class Student(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    courses = models.ManyToManyField(Course)
    marks = models.ManyToManyField(CourseFinalMark)

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'at_students'


class Teacher(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'at_teachers'


class Announcement(models.Model):
    announcement_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=31)
    body = models.TextField()
    post_date = models.DateField(auto_now=True, auto_now_add=True, null=True)
    course = models.ForeignKey(Course)
    
    @classmethod
    def create(cls, course_id, title, body, post_date):
        announcement = cls(course_id=course_id, title=title,
                           body=body, post_date=post_date)
        return announcement

    def __str__(self):
        return self.course_id + ' ' + self.title + ' ' + self.body + ' ' + self.post_date;

    class Meta:
        db_table = 'at_announcements'


class Syllabus(models.Model):
    syllabus_id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='uploads',null=True)
    course = models.ForeignKey(Course)

    def __str__(self):
        return self.file;

    class Meta:
        db_table = 'at_syllabus'


class Policy(models.Model):
    policy_id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='uploads',null=True)
    course = models.ForeignKey(Course)

    def __str__(self):
        return self.policy_id + ' ' + self.file.url;

    class Meta:
        db_table = 'at_policys'


class Lecture(models.Model):
    lecture_id = models.AutoField(primary_key=True)
    lecture_num = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        default=1
    )
    week_num = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        default=1
    )
    title = models.CharField(max_length=63, default='', null=True)
    description = models.TextField(default='', null=True)
    youtube_url = models.URLField(null=True, blank=True)
    vimeo_url = models.URLField(null=True, blank=True)
    bliptv_url = models.URLField(null=True, blank=True)
    VIDEO_PLAYER_CHOICES = (
        (settings.YOUTUBE_VIDEO_PLAYER, 'YouTube'),
        (settings.VIMEO_VIDEO_PLAYER, 'Vimeo')
    )
    preferred_service = models.CharField(
        max_length=1,
        choices=VIDEO_PLAYER_CHOICES,
        default=settings.YOUTUBE_VIDEO_PLAYER
    )
    course = models.ForeignKey(Course)

    def __str__(self):
        return 'Week: ' + str(self.week_num) + ' Lecture: ' + str(self.lecture_num) + ' Title: ' +self.title;

    class Meta:
        db_table = 'at_lectures'


class Exam(models.Model):
    exam_id = models.AutoField(primary_key=True)
    exam_num = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        default=1,
    )
    title = models.CharField(max_length=31, null=True)
    description = models.TextField(null=True)
    start_date = models.DateField(null=True)
    due_date = models.DateField(null=True)
    worth = models.PositiveSmallIntegerField(
        default=0,
        choices=WORTH_PERCENT_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    is_final = models.BooleanField(default=False)
    course = models.ForeignKey(Course)

    def __str__(self):
        return str(self.exam_num) + ' ' + self.title + ' ' + self.description;

    class Meta:
        db_table = 'at_exams'


class ExamSubmission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    percent = models.FloatField(default=0)
    earned_marks = models.FloatField(default=0)
    total_marks = models.PositiveSmallIntegerField(default=0)
    submission_date = models.DateField(null=True)
    is_finished = models.BooleanField(default=False)
    student = models.ForeignKey(Student)
    exam = models.ForeignKey(Exam)

    def __str__(self):
        return self.submission_id + ' ' + self.type;

    class Meta:
        db_table = 'at_exam_submissions'


class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    quiz_num = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(0)],
    )
    title = models.CharField(max_length=31, null=True)
    description = models.TextField(null=True)
    start_date = models.DateField(null=True)
    due_date = models.DateField(null=True)
    worth = models.PositiveSmallIntegerField(
        default=0,
        choices=WORTH_PERCENT_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    course = models.ForeignKey(Course)

    def __str__(self):
        return str(self.quiz_id) + ' ' + str(self.type);

    class Meta:
        db_table = 'at_quizzes'


class QuizSubmission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    percent = models.FloatField(default=0)
    earned_marks = models.FloatField(default=0)
    total_marks = models.PositiveSmallIntegerField(default=0)
    submission_date = models.DateField(null=True)
    is_finished = models.BooleanField(default=False)
    student = models.ForeignKey(Student)
    quiz = models.ForeignKey(Quiz)

    def __str__(self):
        return self.quiz_id + ' ' + self.type;

    class Meta:
        db_table = 'at_quiz_submissions'


class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    assignment_num = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=31, null=True)
    description = models.TextField(null=True)
    start_date = models.DateField(null=True)
    due_date = models.DateField(null=True)
    worth = models.PositiveSmallIntegerField(
        default=0,
        choices=WORTH_PERCENT_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    course = models.ForeignKey(Course)

    def __str__(self):
        return self.assignment_id + ' ' + self.type;

    class Meta:
        db_table = 'at_assignments'


class AssignmentSubmission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    percent = models.FloatField(default=0)
    earned_marks = models.FloatField(default=0)
    total_marks = models.PositiveSmallIntegerField(default=0)
    submission_date = models.DateTimeField(auto_now=True, null=True)
    is_finished = models.BooleanField(default=False)
    student = models.ForeignKey(Student)
    assignment = models.ForeignKey(Assignment)

    def __str__(self):
        return str(assignment_num) + ' ' + str(marks);

    class Meta:
        db_table = 'at_assignment_submissions'


class EssayQuestion(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_num = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        default=1
    )
    title = models.CharField(max_length=31, default='')
    description = models.TextField(default='')
    marks = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        default=1
    )
    question_type = settings.ESSAY_QUESTION_TYPE
    assignment = models.ForeignKey(Assignment, null=True)
    quiz = models.ForeignKey(Quiz, null=True)
    exam = models.ForeignKey(Exam, null=True)

    def __str__(self):
        return self.question_id + ' ' + self.title + ' ' + self.description;

    class Meta:
        db_table = 'at_essay_questions'


class PeerReview(models.Model):
    review_id = models.AutoField(max_length=11, primary_key=True)
    MARK_CHOICES = (
        (0, '0 Star'),
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )
    marks = models.PositiveSmallIntegerField(
        default=0,
        choices=MARK_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    text = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True, auto_now_add=True, null=True)
    user = models.ForeignKey(User)
                          
    def __str__(self):
        return self.course_id + ' ' + self.file_path;

    class Meta:
        db_table = 'at_peer_reviews'


class EssaySubmission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='uploads')
    submission_date = models.DateTimeField(auto_now=True, auto_now_add=True, null=True)
    marks = models.FloatField(
        validators=[MinValueValidator(0)],
        default=0
    )
    student = models.ForeignKey(Student)
    question = models.ForeignKey(EssayQuestion)
    reviews = models.ManyToManyField(PeerReview)
    
    def __str__(self):
        return self.course_id + ' ' + self.file_path;

    class Meta:
        db_table = 'at_essay_submissions'


class MultipleChoiceQuestion(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_num = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        default=1,
    )
    title = models.CharField(max_length=31, default='', blank=True)
    description = models.TextField(default='')
    a = models.CharField(max_length=255, null=True)
    a_is_correct = models.BooleanField(default=False)
    b = models.CharField(max_length=255, null=True)
    b_is_correct = models.BooleanField(default=False)
    c = models.CharField(max_length=255, null=True, blank=True)
    c_is_correct = models.BooleanField(default=False)
    d = models.CharField(max_length=255, null=True, blank=True)
    d_is_correct = models.BooleanField(default=False)
    e = models.CharField(max_length=255, null=True, blank=True)
    e_is_correct = models.BooleanField(default=False)
    f = models.CharField(max_length=255, null=True, blank=True)
    f_is_correct = models.BooleanField(default=False)
    marks = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        default=1,
    )
    question_type = settings.MULTIPLECHOICE_QUESTION_TYPE
    assignment = models.ForeignKey(Assignment, null=True)
    quiz = models.ForeignKey(Quiz, null=True)
    exam = models.ForeignKey(Exam, null=True)

    def __str__(self):
        return self.course_id + ' ' + self.title + ' ' + self.description;

    class Meta:
        db_table = 'at_multiple_choice_questions'

class MultipleChoiceSubmission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    a = models.BooleanField(default=False)
    b = models.BooleanField(default=False)
    c = models.BooleanField(default=False)
    d = models.BooleanField(default=False)
    e = models.BooleanField(default=False)
    f = models.BooleanField(default=False)
    marks = models.FloatField(
        validators=[MinValueValidator(0)],
        default=0,
    )
    submission_date = models.DateTimeField(auto_now=True, auto_now_add=True, null=True)
    student = models.ForeignKey(Student)
    question = models.ForeignKey(MultipleChoiceQuestion)
  
    @classmethod
    def create(cls, assignment_id, exam_id, course_id, student_id, question_num):
        submission = cls(student_id=student_id,
                         course_id=course_id,
                         assignment_id=assignment_id,
                         exam_id=exam_id,
                         question_num=question_num)
        return submission

    def __str__(self):
        return self.course_id + ' ' + self.selected;

    class Meta:
        db_table = 'at_multiple_choice_submissions'


class TrueFalseQuestion(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_num = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        default=1,
    )
    title = models.CharField(max_length=31, default='')
    description = models.TextField(default='')
    true_choice = models.CharField(max_length=127, null=True)
    false_choice = models.CharField(max_length=127, null=True)
    answer = models.BooleanField(default=False)
    marks = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        default=1
    )
    question_type = settings.TRUEFALSE_QUESTION_TYPE
    assignment = models.ForeignKey(Assignment, null=True)
    quiz = models.ForeignKey(Quiz, null=True)
    exam = models.ForeignKey(Exam, null=True)

    def __str__(self):
        return str(self.question_num) + ' ' + self.title + ' ' + self.description;

    class Meta:
        db_table = 'at_true_false_questions'


class TrueFalseSubmission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    answer = models.BooleanField(default=False)
    marks = models.PositiveSmallIntegerField(default=0)
    submission_date = models.DateTimeField(auto_now=True, auto_now_add=True, null=True)
    marks = models.FloatField(
        validators=[MinValueValidator(0)],
        default=0,
    )
    student = models.ForeignKey(Student)
    question = models.ForeignKey(TrueFalseQuestion)
    
    def __str__(self):
        return self.course_id + ' ' + self.selected;

    class Meta:
        db_table = 'at_true_false_submissions'


class ResponseQuestion(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_num = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        default=1,
    )
    title = models.CharField(max_length=31, default='')
    description = models.TextField(default='')
    answer = models.TextField(default='')
    marks = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        default=1
    )
    question_type = settings.RESPONSE_QUESTION_TYPE
    assignment = models.ForeignKey(Assignment, null=True)
    quiz = models.ForeignKey(Quiz, null=True)
    exam = models.ForeignKey(Exam, null=True)

    def __str__(self):
        return self.course_id + ' ' + self.title + ' ' + self.description;

    class Meta:
        db_table = 'at_response_questions'


class ResponseSubmission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    answer = models.TextField(default='')
    marks = models.FloatField(
        validators=[MinValueValidator(0)],
        default=0
    )
    submission_date = models.DateTimeField(auto_now=True, auto_now_add=True, null=True)
    student = models.ForeignKey(Student)
    question = models.ForeignKey(ResponseQuestion)
    reviews = models.ManyToManyField(PeerReview)

    def __str__(self):
        return self.course_id + ' ' + self.response;

    class Meta:
        db_table = 'at_response_submissions'


class CourseDiscussionPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=127)
    text = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True, auto_now_add=True, null=True)
    user = models.ForeignKey(User)
    
    def __str__(self):
        return self.title + ' ' + self.text;

    class Meta:
        db_table = 'at_course_discussion_posts'


class CourseDiscussionThread(models.Model):
    thread_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=127)
    text = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True, auto_now_add=True, null=True)
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)
    posts = models.ManyToManyField(CourseDiscussionPost)
                    
    def __str__(self):
        return self.title + ' ' + self.text;
                    
    class Meta:
        db_table = 'at_course_discussion_threads'
