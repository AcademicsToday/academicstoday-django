from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    name = forms.CharField(
        label='Name',
        max_length=64,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Your Name *'
            }
        ),
    )
    email = forms.EmailField(
        label='Email',
        max_length=64,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Your Email *',
            }
        ),
    )
    phone = forms.CharField(
        label='Phone',
        max_length=31,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Your Phone *'
            }
        ),
    )
    message = forms.CharField(
        label='Message',
        max_length=255,
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder':'Your Message *'
            }
        ),
    )

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', None)
        
        # clean phone by removing all non-numerals
        phone = ''.join(x for x in phone if x.isdigit())
        
        ph_length = str(phone)
        min_length = 10
        max_length = 13
        if len(ph_length) < min_length:
            raise ValidationError('Please enter 10 digit phone number.')
        if len(ph_length) > max_length:
            raise ValidationError('Phone number must be at maxium 13 digits long')
        return phone


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        label='First Name',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}),
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}),
    )
    electronic_mail = forms.EmailField(
        label='Email',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email'}),
    )
    password = forms.CharField(
        label='Password',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Password'}),
    )
    password_repeated = forms.CharField(
        label='Repeat Password',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Password Again'}),
    )
    is_18_or_plus = forms.BooleanField(
        required=False
    )
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

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email'}),
    )
    captcha = CaptchaField()


# Captcha Setup:
# http://django-simple-captcha.readthedocs.org/en/latest/usage.html#installation