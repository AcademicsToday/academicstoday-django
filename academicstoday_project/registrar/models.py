from django.db import models



class CoursePreview(models.Model):
    id = models.AutoField(max_length=11, primary_key=True)
    image_filename = models.CharField(max_length=31)
    title = models.CharField(max_length=63)
    sub_title = models.CharField(max_length=127)
    category = models.CharField(max_length=31)
    description = models.TextField()
    summary = models.TextField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'at_course_previews'



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

