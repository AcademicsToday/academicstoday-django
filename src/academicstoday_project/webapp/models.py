from django.db import models

# Create your models here.

# Developers Note:
#     (1) Database
#     Once you make a change, go to /src/academicstoday_project and type:
#     $ python manage.py makemigrations webapp
#     $ python manage.py migrate webapp
#
#     (2) Reference
#     Go to here to get a list of all the field types we can use.
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

class LandpageTeamMember(models.Model):
    id = models.IntegerField(max_length=11, primary_key=True)
    image_filename = models.CharField(max_length=31)
    full_name = models.CharField(max_length=31)
    role = models.CharField(max_length=31)
    twitter_url = models.CharField(max_length=255)
    facebook_url = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    linkedin_url = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
                                            
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'at_landpage_team_members'