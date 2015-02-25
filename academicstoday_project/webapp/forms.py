from django.db import models
from django import forms

from django.forms import ModelForm
from webapp.models import EssaySubmission

class EssaySubmissionForm(forms.ModelForm):
    class Meta:
        model = EssaySubmission
        exclude = ['id']