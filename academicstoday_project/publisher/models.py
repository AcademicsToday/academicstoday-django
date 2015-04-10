from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import os
from registrar.models import PeerReview

class Publication(models.Model):
    publication_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=127, null=True)
    description = models.TextField(null=True)
    published_date = models.DateField(auto_now= True, null=True)
    file = models.FileField(upload_to='uploads', null=True)
    author = models.ForeignKey(User)
    reviews = models.ManyToManyField(PeerReview)
    
    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super(Publication, self).delete(*args, **kwargs) # Call the "real" delete() method
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'at_publications'