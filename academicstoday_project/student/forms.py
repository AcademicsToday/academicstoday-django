from django.db import models
from django import forms
from django.forms import ModelForm, Textarea, TextInput, NumberInput
from django.forms.extras.widgets import Select, SelectDateWidget
from registrar.models import EssaySubmission
from registrar.models import AssignmentSubmission
from registrar.models import PeerReview
from registrar.models import CourseDiscussionThread
from registrar.models import CourseDiscussionPost


class EssaySubmissionForm(forms.ModelForm):
    class Meta:
        model = EssaySubmission
        fields = '__all__'

    # Function will apply validation on the 'file' upload column in the table.
    def clean_file(self):
        upload = self.cleaned_data['file']
        content_type = upload.content_type
        if content_type in ['application/pdf']:
            if upload._size <= 20971520:
                return upload
            else:
                raise forms.ValidationError("Cannot exceed 20MB size")
        else:
            raise forms.ValidationError("Only accepting PDF files for essays.")


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = '__all__'


class PeerReviewForm(forms.ModelForm):
    class Meta:
        model = PeerReview
        fields = ['marks', 'text']
        labels = {
            'marks': 'Rating',
            'text': 'Review',
        }
        widgets = {
#            'marks': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Title'}),
            'text': Textarea(attrs={'class': u'form-control','placeholder': u'Enter Text'}),
        }


class CourseDiscussionThreadForm(forms.ModelForm):
    class Meta:
        model = CourseDiscussionThread
        fields = ['title', 'text']
        labels = {
            'title': 'Thread Title',
            'text': 'Thread Content',
        }
        widgets = {
            'title': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Title'}),
            'text': Textarea(attrs={'class': u'form-control','placeholder': u'Enter Text'}),
        }


class CourseDiscussionPostForm(forms.ModelForm):
    class Meta:
        model = CourseDiscussionPost
        fields = ['title', 'text']
        labels = {
            'title': 'Post Title',
            'text': 'Post Content',
        }
        widgets = {
            'title': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Title'}),
            'text': Textarea(attrs={'class': u'form-control','placeholder': u'Enter Text'}),
        }