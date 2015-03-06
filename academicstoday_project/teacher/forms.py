from django.db import models
from django import forms

from django.forms import ModelForm, Textarea
from registrar.models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title','body']

        labels = {

        }

        widgets = {
            'body': Textarea(attrs={'cols': 70, 'rows':10}),
        }
