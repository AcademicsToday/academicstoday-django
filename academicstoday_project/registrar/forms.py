from django.db import models
from django import forms
from django.forms.extras.widgets import Select, SelectDateWidget

from django.forms import ModelForm, Textarea
from registrar.models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'sub_title', 'category', 'description', 'start_date', 'finish_date', 'image']
        labels = {
            'sub_title': 'Sub Title',
            'image': 'Upload Image',
            'start_date': 'Start Date',
            'finish_date': 'Finish Date',
        }
        widgets = {
            'description': Textarea(attrs={'cols': 70, 'rows':10}),
            'start_date': SelectDateWidget(),
            'finish_date': SelectDateWidget(),
        }

