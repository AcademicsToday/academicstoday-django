from django.db import models
from django import forms
from django.forms.extras.widgets import Select, SelectDateWidget
from django.conf import settings

from django.forms import ModelForm, Textarea
from registrar.models import FileUpload
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
from registrar.models import Exam

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
        labels = {
            'file': 'PDF Document',
        }


class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ['file']
        labels = {
            'file': 'PDF Document',
        }


class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['lecture_id', 'lecture_num', 'week_num', 'title', 'description', 'youtube_url', 'vimeo_url', 'preferred_service']


class NoteUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['upload_id', 'title', 'description', 'file']
        labels = {
            'file': 'PDF',
        }

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
            raise forms.ValidationError("Only accepting PDF files for course notes.")




class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['assignment_id', 'assignment_num', 'title', 'description', 'start_date', 'due_date', 'worth']
        labels = {
            'worth': 'Worth % of Final Mark',
        }
        widgets = {
            'start_date': SelectDateWidget(),
            'due_date': SelectDateWidget(),
        }


ASSIGNMENT_QUESTION_TYPE_CHOICES = (
    (settings.ESSAY_QUESTION_TYPE, 'Essay'),
    (settings.MULTIPLECHOICE_QUESTION_TYPE, 'Multiple-Choice'),
    (settings.TRUEFALSE_QUESTION_TYPE, 'True/False'),
    (settings.RESPONSE_QUESTION_TYPE, 'Response')
)

class AssignmentQuestionTypeForm(forms.Form):
    question_num = forms.IntegerField(label='Question #', initial=1, widget=forms.NumberInput(attrs={'min': '0', 'max': '100', 'step': '1'}))
    question_type = forms.CharField(label='Question Type', widget=forms.Select(choices=ASSIGNMENT_QUESTION_TYPE_CHOICES))


class EssayQuestionForm(forms.ModelForm):
    class Meta:
        model = EssayQuestion
        fields = ['question_num', 'title', 'description', 'marks']
        labels = {
            'question_num': 'Question #',
        }


class MultipleChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceQuestion
        fields = ['question_num', 'title', 'description', 'a', 'a_is_correct', 'b', 'b_is_correct', 'c', 'c_is_correct', 'd', 'd_is_correct', 'e', 'e_is_correct', 'f', 'f_is_correct', 'marks']
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
        fields = ['question_num', 'title', 'description', 'true_choice', 'false_choice', 'answer', 'marks']
        labels = {
            'question_num': 'Question #',
            'answer': 'Answer is True?',
        }


class ResponseQuestionForm(forms.ModelForm):
    class Meta:
        model = ResponseQuestion
        fields = ['question_num', 'title', 'description', 'answer', 'marks']
        labels = {
            'question_num': 'Question #',
        }

QUIZ_QUESTION_TYPE_CHOICES = (
    (settings.TRUEFALSE_QUESTION_TYPE, 'True/False'),
)

class QuizQuestionTypeForm(forms.Form):
    question_num = forms.IntegerField(label='Question #', initial=1, widget=forms.NumberInput(attrs={'min': '0', 'max': '100', 'step': '1'}))
    question_type = forms.CharField(label='Question Type', widget=forms.Select(choices=QUIZ_QUESTION_TYPE_CHOICES))


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['quiz_num', 'title', 'description', 'start_date', 'due_date', 'worth']
        labels = {
            'quiz_num': 'Quiz #',
            'worth': 'Worth % of Final Mark',
        }
        widgets = {
            'start_date': SelectDateWidget(),
            'due_date': SelectDateWidget(),
        }

EXAM_QUESTION_TYPE_CHOICES = (
    (settings.MULTIPLECHOICE_QUESTION_TYPE, 'Multiple-Choice'),
)

class ExamQuestionTypeForm(forms.Form):
    question_num = forms.IntegerField(label='Question #', initial=1, widget=forms.NumberInput(attrs={'min': '0', 'max': '100', 'step': '1'}))
    question_type = forms.CharField(label='Question Type', widget=forms.Select(choices=EXAM_QUESTION_TYPE_CHOICES))


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['exam_num', 'title', 'description', 'start_date', 'due_date', 'worth', 'is_final']
        labels = {
            'exam_num': 'Exam #',
            'worth': 'Worth % of Final Mark',
            'is_final': 'Is Final Exam',
        }
        widgets = {
            'start_date': SelectDateWidget(),
            'due_date': SelectDateWidget(),
    }
