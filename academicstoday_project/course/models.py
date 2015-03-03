from django.db import models

class Course(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    image_filename = models.CharField(max_length=31)
    title = models.CharField(max_length=63)
    sub_title = models.CharField(max_length=127)
    category = models.CharField(max_length=31)
    paragraph_one = models.CharField(max_length=255)
    paragraph_two = models.CharField(max_length=255)
    paragraph_three = models.CharField(max_length=255)
    start_date = models.DateField()
    finish_date = models.DateField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'at_courses'

class CourseEnrollment(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    course_id = models.IntegerField(max_length=11)
    user_id = models.BigIntegerField()
    
    @classmethod
    def create(cls, course_id, user_id):
        enrollment = cls(course_id=course_id, user_id=user_id)
        return enrollment
    
    def __str__(self):
        return self.course_id + ' ' + self.user_id
    
    class Meta:
        db_table = 'at_course_enrollments'

class Announcement(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    course_id = models.PositiveIntegerField(max_length=11)
    title = models.CharField(max_length=31)
    body = models.TextField()
    post_date = models.DateField()
    
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
    id = models.AutoField(max_length=11, primary_key=True)
    course_id = models.PositiveIntegerField()
    url = models.URLField(default='')
    
    @classmethod
    def create(cls, course_id, url):
        syllabus = cls(course_id=course_id, file_url=file_url)
        return syllabus
    
    def __str__(self):
        return self.course_id + ' ' + self.file_url;
    
    class Meta:
        db_table = 'at_syllabus'

class Policy(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    course_id = models.PositiveIntegerField()
    url = models.URLField(default='')
    
    @classmethod
    def create(cls, course_id, url):
        syllabus = cls(course_id=course_id, file_url=file_url)
        return syllabus
    
    def __str__(self):
        return self.course_id + ' ' + self.file_url;
    
    class Meta:
        db_table = 'at_policys'

class Week(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    course_id = models.PositiveIntegerField()
    week_num = models.PositiveSmallIntegerField(max_length=7)
    title = models.CharField(max_length=31)
    description = models.TextField()
    
    def __str__(self):
        return self.course_id + ' ' + self.file_url;
    
    class Meta:
        db_table = 'at_weeks'

class Lecture(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    course_id = models.PositiveIntegerField()
    week_num = models.PositiveSmallIntegerField(max_length=7)
    lecture_num = models.PositiveSmallIntegerField(max_length=7, default=0)
    title = models.CharField(max_length=31, default='',null=True)
    description = models.TextField(default='',null=True)
    youtube_url = models.URLField(default='',null=True)
    vimeo_url = models.URLField(default='',null=True)
    bliptv_url = models.URLField(default='',null=True)
    preferred_service = models.CharField(max_length=31)
    
    def __str__(self):
        return self.course_id + ' ' + self.file_url;
    
    class Meta:
        db_table = 'at_lectures'

class Assignment(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    course_id = models.PositiveIntegerField()
    order_num = models.PositiveSmallIntegerField(default=0)
    type = models.PositiveSmallIntegerField()
    due_date = models.DateField(null=True)

    def __str__(self):
        return self.course_id + ' ' + self.type;
    
    class Meta:
        db_table = 'at_assignments'


class AssignmentSubmission(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    assignment_id = models.PositiveIntegerField()
    student_id = models.BigIntegerField()
    course_id = models.PositiveIntegerField()
    order_num = models.PositiveSmallIntegerField(default=0)
    type = models.PositiveSmallIntegerField()
    marks = models.PositiveSmallIntegerField(default=0)
    submission_date = models.DateField(null=True)
    is_marked = models.BooleanField(default=False)
    
    @classmethod
    def create(cls, student_id, course_id, assignment_id, type, order_num):
        submission = cls(
            student_id=student_id,
            course_id=course_id,
            assignment_id=assignment_id,
            type=type,
            order_num=order_num
        )
        return submission
    
    def __str__(self):
        return self.course_id + ' ' + self.type;
    
    class Meta:
        db_table = 'at_assignment_submissions'


class EssayQuestion(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    assignment_id = models.PositiveIntegerField()
    course_id = models.PositiveIntegerField()
    question_num = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=31, default='')
    description = models.TextField(default='')
    
    def __str__(self):
        return self.course_id + ' ' + self.title + ' ' + self.description;
    
    class Meta:
        db_table = 'at_essay_questions'

class EssaySubmission(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    assignment_id = models.BigIntegerField()
    student_id = models.BigIntegerField()
    course_id = models.PositiveIntegerField()
    file = models.FileField(upload_to='uploads')
    submission_date = models.DateTimeField(auto_now=True, auto_now_add=True, null=True)
    is_marked = models.BooleanField(default=False)
    
    @classmethod
    def create(cls, student_id, course_id, assignment_id, file):
        submission = cls(student_id=student_id,
                         course_id=course_id,
                         assignment_id=assignment_id,
                         file=file)
        return submission
    
    def __str__(self):
        return self.course_id + ' ' + self.file_path;
    
    class Meta:
        db_table = 'at_essay_submissions'

class MultipleChoiceQuestion(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    exam_id = models.PositiveIntegerField(default=0)
    assignment_id = models.PositiveIntegerField()
    course_id = models.PositiveIntegerField()
    question_num = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=31, default='')
    description = models.TextField(default='')
    json_choices = models.CharField(max_length=1055, default='{}')
    json_answers = models.CharField(max_length=127, default='{}')
    
    def __str__(self):
        return self.course_id + ' ' + self.title + ' ' + self.description;
    
    class Meta:
        db_table = 'at_multiple_choice_questions'

class MultipleChoiceSubmission(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    student_id = models.BigIntegerField()
    assignment_id = models.PositiveIntegerField()
    exam_id = models.PositiveIntegerField(default=0)
    course_id = models.PositiveIntegerField()
    question_num = models.PositiveSmallIntegerField(default=0)
    json_answers = models.CharField(max_length=127, default='{}')
    marks = models.PositiveSmallIntegerField(default=0)
    submission_date = models.DateTimeField(auto_now=True, auto_now_add=True, null=True)
    is_marked = models.BooleanField(default=False)
    
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
    id = models.AutoField(max_length=11, primary_key=True)
    assignment_id = models.PositiveIntegerField(default=0)
    quiz_id = models.PositiveIntegerField(default=0)
    course_id = models.PositiveIntegerField()
    question_num = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=31, default='')
    description = models.TextField(default='')
    true_choice = models.CharField(max_length=127, null=True)
    false_choice = models.CharField(max_length=127, null=True)
    answer = models.BooleanField(default=False)
    
    def __str__(self):
        return self.course_id + ' ' + self.title + ' ' + self.description;
    
    class Meta:
        db_table = 'at_true_false_questions'


class TrueFalseSubmission(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    student_id = models.BigIntegerField()
    assignment_id = models.PositiveIntegerField(default=0)
    quiz_id = models.PositiveIntegerField(default=0)
    course_id = models.PositiveIntegerField()
    question_num = models.PositiveSmallIntegerField(default=0)
    answer = models.BooleanField(default=False)
    marks = models.PositiveSmallIntegerField(default=0)
    submission_date = models.DateTimeField(auto_now=True, auto_now_add=True, null=True)
    is_marked = models.BooleanField(default=False)
    
    @classmethod
    def create(cls, assignment_id, quiz_id, course_id, student_id, question_num):
        submission = cls(student_id=student_id,
                         course_id=course_id,
                         assignment_id=assignment_id,
                         quiz_id=quiz_id,
                         question_num=question_num)
        return submission
    
    def __str__(self):
        return self.course_id + ' ' + self.selected;
    
    class Meta:
        db_table = 'at_true_false_submissions'


class ResponseQuestion(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    assignment_id = models.PositiveIntegerField()
    course_id = models.PositiveIntegerField()
    question_num = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=31, default='')
    description = models.TextField(default='')
    answer = models.TextField(default='')
    
    def __str__(self):
        return self.course_id + ' ' + self.title + ' ' + self.description;
    
    class Meta:
        db_table = 'at_response_questions'


class ResponseSubmission(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    student_id = models.BigIntegerField()
    assignment_id = models.PositiveIntegerField()
    course_id = models.PositiveIntegerField()
    question_num = models.PositiveSmallIntegerField(default=0)
    answer = models.TextField(default='')
    marks = models.PositiveSmallIntegerField(default=0)
    submission_date = models.DateTimeField(auto_now=True, auto_now_add=True, null=True)
    is_marked = models.BooleanField(default=False)

    @classmethod
    def create(cls, assignment_id, course_id, student_id, question_num):
        submission = cls(student_id=student_id,
                         course_id=course_id,
                         assignment_id=assignment_id,
                         question_num=question_num)
        return submission
    
    def __str__(self):
        return self.course_id + ' ' + self.response;
    
    class Meta:
        db_table = 'at_response_submissions'


class Quiz(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    course_id = models.PositiveIntegerField()
    order_num = models.PositiveSmallIntegerField(default=0)
    type = models.PositiveSmallIntegerField()
    due_date = models.DateField(null=True)
    
    def __str__(self):
        return self.course_id + ' ' + self.type;
    
    class Meta:
        db_table = 'at_quizzes'


class QuizSubmission(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    quiz_id = models.PositiveIntegerField()
    student_id = models.BigIntegerField()
    course_id = models.PositiveIntegerField()
    order_num = models.PositiveSmallIntegerField(default=0)
    type = models.PositiveSmallIntegerField()
    marks = models.PositiveSmallIntegerField(default=0)
    submission_date = models.DateField(null=True)
    is_marked = models.BooleanField(default=False)
    
    @classmethod
    def create(cls, student_id, course_id, quiz_id, type, order_num):
        submission = cls(
            student_id=student_id,
            course_id=course_id,
            quiz_id=quiz_id,
            type=type,
            order_num=order_num
        )
        return submission
    
    def __str__(self):
        return self.quiz_id + ' ' + self.type;
    
    class Meta:
        db_table = 'at_quiz_submissions'


class Exam(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    course_id = models.PositiveIntegerField()
    order_num = models.PositiveSmallIntegerField(default=0)
    type = models.PositiveSmallIntegerField()
    start_date = models.DateField(null=True)
    due_date = models.DateField(null=True)
  
    def __str__(self):
        return self.course_id + ' ' + self.type;
    
    class Meta:
        db_table = 'at_exams'


class ExamSubmission(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    exam_id = models.PositiveIntegerField()
    student_id = models.BigIntegerField()
    course_id = models.PositiveIntegerField()
    order_num = models.PositiveSmallIntegerField(default=0)
    type = models.PositiveSmallIntegerField()
    marks = models.PositiveSmallIntegerField(default=0)
    submission_date = models.DateField(null=True)
    is_marked = models.BooleanField(default=False)

    @classmethod
    def create(cls, student_id, course_id, exam_id, type, order_num):
        submission = cls(
            student_id=student_id,
            course_id=course_id,
            exam_id=exam_id,
            type=type,
            order_num=order_num
        )
        return submission
    
    def __str__(self):
        return self.quiz_id + ' ' + self.type;
    
    class Meta:
        db_table = 'at_exam_submissions'

