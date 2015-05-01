from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import os
from account.models import Student
from account.models import Teacher

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

COURSE_CATEGORY_TYPES = (
    ('Aeronautics & Astronautics', 'Aeronautics & Astronautics'),
    ('Anesthesia', 'Anesthesia'),
    ('Anthropology', 'Anthropology'),
    ('Applied Physics', 'Applied Physics'),
    ('Art or Art History', 'Art & Art History'),
    ('Astrophysics', 'Astrophysics'),
    ('Biochemistry', 'Biochemistry'),
    ('Bioengineering', 'Bioengineering'),
    ('Biology', 'Biology'),
    ('Business', 'Business'),
    ('Cardiothoracic Surgery', 'Cardiothoracic Surgery'),
    ('Chemical and Systems Biology', 'Chemical and Systems Biology'),
    ('Chemical Engineering', 'Chemical Engineering'),
    ('Chemistry', 'Chemistry'),
    ('Civil and Environmental Engineering', 'Civil and Environmental Engineering'),
    ('Classics', 'Classics'),
    ('Communication', 'Communication'),
    ('Comparative Literature', 'Comparative Literature'),
    ('Comparative Medicine', 'Comparative Medicine'),
    ('Computer Science', 'Computer Science'),
    ('Dermatology', 'Dermatology'),
    ('Developmental Biology', 'Developmental Biology'),
    ('East Asian Languages and Cultures', 'East Asian Languages and Cultures'),
    ('Economics', 'Economics'),
    ('Education', 'Education'),
    ('Electrical Engineering', 'Electrical Engineering'),
    ('English', 'English'),
    ('French', 'French'),
    ('Genetics', 'Genetics'),
    ('General Eduction', 'General Education'),
    ('Geological and Environmental Sciences', 'Geological and Environmental Sciences'),
    ('Geophysics', 'Geophysics'),
    ('Health', 'Health'),
    ('History', 'History'),
    ('Latin American Cultures', 'Latin American Cultures'),
    ('Law School', 'Law School'),
    ('Linguistics', 'Linguistics'),
    ('Management', 'Management'),
    ('Materials Science', 'Materials Science'),
    ('Mathematics', 'Mathematics'),
    ('Mechanical Engineering', 'Mechanical Engineering'),
    ('Medicine', 'Medicine'),
    ('Microbiology and Immunology', 'Microbiology and Immunology'),
    ('Molecular and Cellular Physiology', 'Molecular and Cellular Physiology'),
    ('Music', 'Music'),
    ('Neurobiology', 'Neurobiology'),
    ('Neurology', 'Neurology'),
    ('Neurosurgery', 'Neurosurgery'),
    ('Obstetrics and Gynecology', 'Obstetrics and Gynecology'),
    ('Ophthalmology', 'Ophthalmology'),
    ('Orthopaedic Surgery', 'Orthopaedic Surgery'),
    ('Other', 'Other'),
    ('Otolaryngology', 'Otolaryngology'),
    ('Pathology', 'Pathology'),
    ('Pediatrics', 'Pediatrics'),
    ('Philosophy', 'Philosophy'),
    ('Physics', 'Physics'),
    ('Political Science', 'Political Science'),
    ('Psychiatry', 'Psychiatry'),
    ('Psychology', 'Psychology'),
    ('Radiation Oncology', 'Radiation Oncology'),
    ('Radiology', 'Radiology'),
    ('Religious Studies', 'Religious Studies'),
    ('Slavic Languages and Literature', 'Slavic Languages and Literature'),
    ('Sociology', 'Sociology'),
    ('Statistics', 'Statistics'),
    ('Surgery', 'Surgery'),
    ('Theater and Performance Studies', 'Theater and Performance Studies'),
    ('Urology', 'Urology'),
)


class FileUpload(models.Model):
    upload_id = models.AutoField(primary_key=True)
    type = models.PositiveSmallIntegerField(default=settings.UNKNOWN_FILE_UPLOAD_TYPE)
    title = models.CharField(max_length=127, null=True)
    description = models.TextField(null=True)
    upload_date = models.DateField(auto_now= True, null=True)
    file = models.FileField(upload_to='uploads', null=True)
    user = models.ForeignKey(User)
    
    def delete(self, *args, **kwargs):
        """
            Overrided delete functionality to include deleting the local file
            that we have stored on the system. Currently the deletion funciton
            is missing this functionality as it's our responsibility to handle
            the local files.
        """
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super(FileUpload, self).delete(*args, **kwargs) # Call the "real" delete() method
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'at_file_uploads'


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=127)
    sub_title = models.CharField(max_length=127)
    category = models.CharField(max_length=127, choices=COURSE_CATEGORY_TYPES, default='General Education')
    description = models.TextField(null=True)
    start_date = models.DateField(null=True)
    finish_date = models.DateField(null=True)
    is_official = models.BooleanField(default=False)
    status = models.PositiveSmallIntegerField(default=settings.COURSE_UNAVAILABLE_STATUS)
    image = models.ImageField(upload_to='uploads', null=True, blank=True)
    students = models.ManyToManyField(Student)
    teacher = models.ForeignKey(Teacher)

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super(Course, self).delete(*args, **kwargs) # Call the "real" delete() method

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
    submission_date = models.DateField(auto_now=True, null=True)
    course = models.ForeignKey(Course)

    def __str__(self):
        return str(self.review_date) + ' ' + str(self.course)

    class Meta:
        db_table = 'at_course_submissions'


class CourseSetting(models.Model):
    settings_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course)
    final_exam_percent = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=50
    )
    course_percent = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=50
    )
    
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
    is_public = models.BooleanField(default=False)
    course = models.ForeignKey(Course)
    student = models.ForeignKey(Student)
        
    def __str__(self):
        return str(self.student) + " " + str(self.course) + " " + str(self.percent) + "%"
                                
    class Meta:
        db_table = 'at_course_final_marks'


class Announcement(models.Model):
    announcement_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=31)
    body = models.TextField()
    post_date = models.DateField(auto_now_add=True, null=True)
    course = models.ForeignKey(Course)
    
    @classmethod
    def create(cls, course_id, title, body, post_date):
        announcement = cls(course_id=course_id, title=title,
                           body=body, post_date=post_date)
        return announcement

    def __str__(self):
        return str(self.announcement_id) + ' ' + self.title + ' ' + self.body + ' ' + str(self.post_date);

    class Meta:
        db_table = 'at_announcements'


class Syllabus(models.Model):
    syllabus_id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='uploads',null=True)
    course = models.ForeignKey(Course)

    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                 os.remove(self.file.path)
        super(Syllabus, self).delete(*args, **kwargs) # Call the "real" delete() method

    def __str__(self):
        return str(self.syllabus_id) + ' ' + self.file.url;

    class Meta:
        db_table = 'at_syllabus'


class Policy(models.Model):
    policy_id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='uploads',null=True)
    course = models.ForeignKey(Course)

    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super(Policy, self).delete(*args, **kwargs) # Call the "real" delete() method

    def __str__(self):
        return str(self.policy_id) + ' ' + self.file.url;

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
    notes = models.ManyToManyField(FileUpload)

    def delete(self, *args, **kwargs):
        for note in self.notes.all():
            note.delete()
        super(Lecture, self).delete(*args, **kwargs) # Call the "real" delete() method

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
    submission_date = models.DateField(auto_now=True, null=True)
    is_finished = models.BooleanField(default=False)
    student = models.ForeignKey(Student)
    exam = models.ForeignKey(Exam)

    def __str__(self):
        return str(self.submission_id) + ' ' + str(self.percent) + '% ' + \
        str(self.earned_marks) + '/' + str(self.total_marks)

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
        return str(self.quiz_id) + ' ' + self.title + ' ' + str(self.worth);

    class Meta:
        db_table = 'at_quizzes'


class QuizSubmission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    percent = models.FloatField(default=0)
    earned_marks = models.FloatField(default=0)
    total_marks = models.PositiveSmallIntegerField(default=0)
    submission_date = models.DateField(auto_now=True, null=True)
    is_finished = models.BooleanField(default=False)
    student = models.ForeignKey(Student)
    quiz = models.ForeignKey(Quiz)

    def __str__(self):
        return str(self.submission_id) + ' ' + str(self.percent) + '%'

    class Meta:
        db_table = 'at_quiz_submissions'


class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    assignment_num = models.PositiveSmallIntegerField(
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
    course = models.ForeignKey(Course)

    def __str__(self):
        return str(self.assignment_id) + ' ' + self.title;

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
        return str(self.submission_id) + ' ' + str(self.percent) + '%';

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
        return str(self.question_id) + ' ' + self.title + ' ' + self.description;

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
    date = models.DateTimeField(auto_now=True, null=True)
    user = models.ForeignKey(User)
                          
    def __str__(self):
        return str(self.review_id) + ' ' + self.text;

    class Meta:
        db_table = 'at_peer_reviews'


class EssaySubmission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='uploads')
    submission_date = models.DateTimeField(auto_now=True, null=True)
    marks = models.FloatField(
        validators=[MinValueValidator(0)],
        default=0
    )
    student = models.ForeignKey(Student)
    question = models.ForeignKey(EssayQuestion)
    reviews = models.ManyToManyField(PeerReview)
    
    def delete(self, *args, **kwargs):
        for review in self.reviews.all():
            review.delete()

        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super(EssaySubmission, self).delete(*args, **kwargs) # Call the "real" delete() method
    
    def __str__(self):
        return str(self.submission_id) + ' ' + self.file.url + ' By ' + str(self.student)

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
        return str(self.question_id) + ' ' + self.title + ' ' + self.description;

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
    submission_date = models.DateTimeField(auto_now=True, null=True)
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
        return str(self.submission_id) + ' ' + self.question + ' By ' + self.student

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
        return str(self.question_num) + ' ' + self.title + ' ' + self.description

    class Meta:
        db_table = 'at_true_false_questions'


class TrueFalseSubmission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    answer = models.BooleanField(default=False)
    marks = models.PositiveSmallIntegerField(default=0)
    submission_date = models.DateTimeField(auto_now=True, null=True)
    marks = models.FloatField(
        validators=[MinValueValidator(0)],
        default=0,
    )
    student = models.ForeignKey(Student)
    question = models.ForeignKey(TrueFalseQuestion)
    
    def __str__(self):
        return str(self.submission_id) + ' ' + self.question + ' By ' + self.student

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
        return str(self.question_id) + ' ' + self.title + ' ' + self.description;

    class Meta:
        db_table = 'at_response_questions'


class ResponseSubmission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    answer = models.TextField(default='')
    marks = models.FloatField(
        validators=[MinValueValidator(0)],
        default=0
    )
    submission_date = models.DateTimeField(auto_now=True, null=True)
    student = models.ForeignKey(Student)
    question = models.ForeignKey(ResponseQuestion)
    reviews = models.ManyToManyField(PeerReview)

    def delete(self, *args, **kwargs):
        for review in self.review.all():
            review.delete()
        super(ResponseSubmission, self).delete(*args, **kwargs)

    def __str__(self):
        return str(self.submission_id) + ' ' + self.response + ' By ' + self.student

    class Meta:
        db_table = 'at_response_submissions'


class CourseDiscussionPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=127)
    text = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True, null=True)
    user = models.ForeignKey(User)
    
    def __str__(self):
        return self.title + ' ' + self.text;

    class Meta:
        db_table = 'at_course_discussion_posts'


class CourseDiscussionThread(models.Model):
    thread_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=127)
    text = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True, null=True)
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)
    posts = models.ManyToManyField(CourseDiscussionPost)
                    
    def __str__(self):
        return self.title + ' ' + self.text;
                    
    class Meta:
        db_table = 'at_course_discussion_threads'

    def delete(self, *args, **kwargs):
        for post in self.posts.all():
            post.delete()
        super(CourseDiscussionThread, self).delete(*args, **kwargs)
