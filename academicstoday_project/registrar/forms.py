from django.db import models
from django import forms

from django.forms import ModelForm
from course.models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'sub_title', 'category', 'description', 'start_date', 'finish_date', 'image']

    # Function will apply validation on the 'file' upload column in the table.
    def clean_image(self):
        upload = self.cleaned_data['image']
        content_type = upload.content_type
        if content_type in ['application/png', 'application/x-png']:
            if upload._size <= 20971520:
                return upload
            else:
                raise forms.ValidationError("Cannot exceed 20MB size")
        else:
            raise forms.ValidationError("Only accepting PNG files for essays.")
