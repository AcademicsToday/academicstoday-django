from django.db import models
from django import forms

from django.forms import ModelForm
from course.models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'sub_title', 'category', 'description', 'start_date', 'finish_date']
