from django.db import models
from django import forms
from captcha.fields import CaptchaField

class RegisterForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    electronic_mail = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=100)
    password_repeated = forms.CharField(label='Repeat Password', max_length=100)
    is_18_or_plus = forms.BooleanField(required=False)
    captcha = CaptchaField()

    def clean_is_18_or_plus(self):
        data = self.cleaned_data
        if data.get('is_18_or_plus'):
            return data
        else:
           raise forms.ValidationError("You must be 18 or over.")

    def clean_password_repeated(self):
        password = self.cleaned_data['password'] # cleaned_data dictionary has the
        # the valid fields
        password_repeated = self.cleaned_data['password_repeated']
        if password != password_repeated:
            raise forms.ValidationError("Passwords do not match.")
        return password_repeated

# Captcha Setup:
# http://django-simple-captcha.readthedocs.org/en/latest/usage.html#installation