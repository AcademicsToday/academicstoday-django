from django.db import models
from django import forms

from django.forms import ModelForm, Textarea
from course.models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'sub_title', 'category', 'description', 'start_date', 'finish_date', 'file']

        labels = {
            'file': 'Image',
        }

        widgets = {
            'description': Textarea(attrs={'cols': 70, 'rows':10}),
        }

    # Function will apply validation on the 'file' upload column in the table.
    def clean_file(self):
        upload = self.cleaned_data['file']
        content_type = upload.content_type
        if content_type in ['image/png']:
            if upload._size <= 20971520:
                return upload
            else:
                raise forms.ValidationError("Cannot exceed 20MB size")
        else:
            raise forms.ValidationError("Only accepting PNG files for course image.")
