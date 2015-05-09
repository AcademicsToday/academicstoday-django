from django.db import models
from registrar.models import Course

# Create your models here.

# Developers Note:
#     (1) Database
#     Once you make a change, go to /src/academicstoday_project and type:
#     $ python manage.py makemigrations landpage
#     $ python manage.py migrate landpage
#
#     (2) Field Types
#     https://docs.djangoproject.com/en/1.7/ref/models/fields/#field-types
#
#     (3) Meta Options
#     https://docs.djangoproject.com/en/1.7/ref/models/options/
#
#     (4) Query Sets
#     https://docs.djangoproject.com/en/1.7/ref/models/querysets/
#
#     (5) Models
#     https://docs.djangoproject.com/en/1.7/topics/db/models/
#
#     (6) Model Instances
#     https://docs.djangoproject.com/en/1.7/ref/models/instances/
#


class LandpageTeamMember(models.Model):
    id = models.AutoField(primary_key=True)
    image_filename = models.CharField(max_length=31)
    full_name = models.CharField(max_length=31)
    role = models.CharField(max_length=31)
    twitter_url = models.CharField(max_length=255, null=True)
    facebook_url = models.CharField(max_length=255, null=True)
    image_filename = models.CharField(max_length=255, null=True)
    linkedin_url = models.CharField(max_length=255, null=True)
    github_url = models.CharField(max_length=255, null=True)
    google_url = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = 'at_landpage_team_members'


class LandpageCoursePreview(models.Model):
    id = models.AutoField(primary_key=True)
    image_filename = models.CharField(max_length=31)
    title = models.CharField(max_length=127)
    category = models.CharField(max_length=31)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'at_landpage_course_previews'

class LandpageTopPickCourse(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course)
    
    def __str__(self):
        return self.course
    
    class Meta:
        db_table = 'at_landpage_top_pick_courses'


class CoursePreview(models.Model):
    id = models.AutoField(primary_key=True)
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


class LandpageContactMessage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=127)
    email = models.EmailField()
    phone = models.CharField(max_length=63)
    message = models.TextField()
    posted_date = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.name + " " + self.email + " " + self.phone
    
    class Meta:
        db_table = 'at_landpage_contact_message'


class LandpagePartner(models.Model):
    id = models.AutoField(primary_key=True)
    image_filename = models.CharField(max_length=31)
    title = models.CharField(max_length=127)
    url = models.URLField()
    
    def __str__(self):
        return self.title + ' ' + self.url
    
    class Meta:
        db_table = 'at_landpage_partners'