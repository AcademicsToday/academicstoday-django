from django.db import models
from django import forms

from django.forms import ModelForm
from account.models import PrivateMessage


class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['from_address', 'title', 'text']
        labels = {
            'from_address': 'From',
        }