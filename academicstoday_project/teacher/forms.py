from django.db import models
from django import forms
from django.forms.extras.widgets import Select, SelectDateWidget
from django.conf import settings

from django.forms import ModelForm, Textarea
from registrar.models import Announcement
from registrar.models import Syllabus
from registrar.models import Policy
from registrar.models import Lecture
from registrar.models import Assignment
from registrar.models import EssayQuestion
from registrar.models import MultipleChoiceQuestion
from registrar.models import TrueFalseQuestion
from registrar.models import ResponseQuestion
from registrar.models import Quiz

# Django Forms
# https://docs.djangoproject.com/en/1.7/topics/forms/
#
# Django Widgets
# https://docs.djangoproject.com/en/1.7/ref/forms/widgets/
#

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
        fields = ['assignment_id', 'assignment_num', 'title', 'description', 'start_date', 'due_date']
        widgets = {
            'start_date': SelectDateWidget(),
            'due_date': SelectDateWidget(),
        }


QUESTION_TYPE_CHOICES = ((settings.ESSAY_QUESTION_TYPE, 'Essay'),
                         (settings.MULTIPLECHOICE_QUESTION_TYPE, 'Multiple-Choice'),
                         (settings.TRUEFALSE_QUESTION_TYPE, 'True/False'),
                         (settings.RESPONSE_QUESTION_TYPE, 'Response'))

class QuestionTypeForm(forms.Form):
    question_num = forms.IntegerField(label='Question #', initial=1, widget=forms.NumberInput(attrs={'min': '0', 'max': '100', 'step': '1'}))
    question_type = forms.CharField(label='Question Type', widget=forms.Select(choices=QUESTION_TYPE_CHOICES))


class EssayQuestionForm(forms.ModelForm):
    class Meta:
        model = EssayQuestion
        fields = ['question_num', 'title', 'description']
        labels = {
            'question_num': 'Question #',
        }


class MultipleChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceQuestion
        fields = ['question_num', 'title', 'description', 'a', 'a_is_correct', 'b', 'b_is_correct', 'c', 'c_is_correct', 'd', 'd_is_correct', 'e', 'e_is_correct', 'f', 'f_is_correct']
        labels = {
            'question_num': 'Question #',
            'a': 'Option A)',
            'b': 'Option B)',
            'c': 'Option C)',
            'd': 'Option D)',
            'e': 'Option E)',
            'f': 'Option F)',
        }


class TrueFalseQuestionForm(forms.ModelForm):
    class Meta:
        model = TrueFalseQuestion
        fields = ['question_num', 'title', 'description', 'true_choice', 'false_choice', 'answer']
        labels = {
            'question_num': 'Question #',
            'answer': 'Answer is True?',
        }


class ResponseQuestionForm(forms.ModelForm):
    class Meta:
        model = ResponseQuestion
        fields = ['question_num', 'title', 'description', 'answer']
        labels = {
            'question_num': 'Question #',
        }


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['quiz_num', 'title', 'description', 'start_date', 'due_date']
        widgets = {
            'start_date': SelectDateWidget(),
            'due_date': SelectDateWidget(),
    }
