from django.db import models
from django.contrib.auth.models import User


class PrivateMessage(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=127)
    text = models.TextField()
    sent_date = models.DateField(auto_now_add=True, null=True)
    to_address = models.CharField(max_length=255)
    from_address = models.CharField(max_length=255)
    
    def __str__(self):
        return "From: " + self.from_address + " To: " + self.to_address + " Title: " + self.title
    
    class Meta:
        db_table = 'at_private_messages'


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    
    def __str__(self):
        return self.user.first_name + " " + \
                          self.user.last_name 
    
    class Meta:
        db_table = 'at_students'


class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    
    def __str__(self):
        return self.user.first_name + " " + \
            self.user.last_name + " "
    
    class Meta:
        db_table = 'at_teachers'