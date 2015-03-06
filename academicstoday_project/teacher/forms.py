from django.db import models
from django import forms

from django.forms import ModelForm, Textarea
from registrar.models import Announcement
from registrar.models import Syllabus
from registrar.models import Policy
from registrar.models import Lecture
from registrar.models import Assignment

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title','body']

        labels = {

        }

        widgets = {
            'body': Textarea(attrs={'cols': 70, 'rows':10}),
        }


class SyllabusForm(forms.ModelForm):
    class Meta:
        model = Syllabus
        fields = ['file']


class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ['file']


class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['lecture_id', 'lecture_num', 'week_num', 'title', 'description', 'youtube_url', 'vimeo_url', 'preferred_service']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['assignment_id', 'assignment_num', 'type', 'due_date']