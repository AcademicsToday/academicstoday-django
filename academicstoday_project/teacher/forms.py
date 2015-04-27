from django.db import models
from django import forms
from django.forms.extras.widgets import Select, SelectDateWidget
from django.conf import settings
from django.forms import ModelForm, Textarea, TextInput, NumberInput
from django.forms.extras.widgets import Select, SelectDateWidget
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


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title','body']
        labels = {

        }
        widgets = {
            'title': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Title'}),
            'body': Textarea(attrs={'class': u'form-control','placeholder': u'Enter Description'}),
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
        labels = {
            'lecture_num': 'Lecture Number',
            'week_num': 'Week Number',
            'youtube_url': 'YouTube URL',
            'vimeo_url': 'Vimeo URL',
        }
        widgets = {
            'lecture_num': NumberInput(attrs={'class': u'form-control','placeholder': u'Enter Lecture Number'}),
            'week_num': NumberInput(attrs={'class': u'form-control','placeholder': u'Enter Week Number'}),
            'title': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Title'}),
            'description': Textarea(attrs={'class': u'form-control','placeholder': u'Enter Description'}),
            'youtube_url': TextInput(attrs={'class': u'form-control','placeholder': u'Enter YouTube URL'}),
            'vimeo_url': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Vimeo URL'}),
            'preferred_service': Select(attrs={'class': u'form-control'}),
        }

    def clean(self):
        youtube_url = self.cleaned_data['youtube_url']
        if youtube_url is not '':
            if "https://www.youtube.com/embed/" not in youtube_url:
                raise forms.ValidationError("YouTube URL needs to be a embedded URL.")


class NoteUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['upload_id', 'title', 'description', 'file']
        labels = {
            'file': 'PDF',
        }
        widgets = {
            'title': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Title'}),
            'description': Textarea(attrs={'class': u'form-control','placeholder': u'Enter Description'}),
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
            'assignment_num': 'Assignment Number',
            'worth': 'Worth % of Final Mark',
        }
        widgets = {
            'assignment_num': NumberInput(attrs={'class': u'form-control','placeholder': u'Enter Assignment Number'}),
            'title': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Title'}),
            'description': Textarea(attrs={'class': u'form-control','placeholder': u'Enter Description'}),
            'start_date': SelectDateWidget(),
            'due_date': SelectDateWidget(),
            'worth': Select(attrs={'class': u'form-control'}),
        }


ASSIGNMENT_QUESTION_TYPE_CHOICES = (
    (settings.ESSAY_QUESTION_TYPE, 'Essay'),
    (settings.MULTIPLECHOICE_QUESTION_TYPE, 'Multiple-Choice'),
    (settings.TRUEFALSE_QUESTION_TYPE, 'True/False'),
    (settings.RESPONSE_QUESTION_TYPE, 'Response')
)

class AssignmentQuestionTypeForm(forms.Form):
    question_num = forms.IntegerField(label='Question #', initial=1, widget=forms.NumberInput(attrs={'class': u'form-control','placeholder': u'Enter Question Number', 'min': '0', 'max': '100', 'step': '1'}))
    question_type = forms.CharField(label='Question Type', widget=forms.Select(attrs={'class': u'form-control'}, choices=ASSIGNMENT_QUESTION_TYPE_CHOICES))


class EssayQuestionForm(forms.ModelForm):
    class Meta:
        model = EssayQuestion
        fields = ['question_num', 'title', 'description', 'marks']
        labels = {
            'question_num': 'Question #',
        }
        widgets = {
            'question_num': NumberInput(attrs={'class': u'form-control','placeholder': u'Enter Question Number'}),
            'title': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Title'}),
            'description': Textarea(attrs={'class': u'form-control','placeholder': u'Enter Description'}),
            'start_date': SelectDateWidget(),
            'due_date': SelectDateWidget(),
            'marks': NumberInput(attrs={'class': u'form-control','placeholder': u'Enter Marks'}),
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
        widgets = {
            'question_num': NumberInput(attrs={'class': u'form-control','placeholder': u'Enter Question Number'}),
            'title': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Title'}),
            'description': Textarea(attrs={'class': u'form-control','placeholder': u'Enter Description'}),
            'a': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Option A Description'}),
            'b': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Option B Description'}),
            'c': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Option C Description'}),
            'd': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Option D Description'}),
            'e': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Option E Description'}),
            'f': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Option F Description'}),
            'marks': NumberInput(attrs={'class': u'form-control','placeholder': u'Enter Marks'}),
        }

    def clean(self):
        cleaned_data = super(MultipleChoiceQuestionForm, self).clean()
        a_is_correct = cleaned_data.get("a_is_correct")
        b_is_correct = cleaned_data.get("b_is_correct")
        c_is_correct = cleaned_data.get("c_is_correct")
        d_is_correct = cleaned_data.get("d_is_correct")
        e_is_correct = cleaned_data.get("e_is_correct")
        f_is_correct = cleaned_data.get("f_is_correct")
        
        # Validate to ensure at least a single correct answer exists
        answer_count = 0
        if a_is_correct:
            answer_count += 1
        if b_is_correct:
            answer_count += 1
        if c_is_correct:
            answer_count += 1
        if d_is_correct:
            answer_count += 1
        if e_is_correct:
            answer_count += 1
        if f_is_correct:
            answer_count += 1
        if answer_count <= 0:
            raise forms.ValidationError("Minimum of one correc answer must exist.")


class TrueFalseQuestionForm(forms.ModelForm):
    class Meta:
        model = TrueFalseQuestion
        fields = ['question_num', 'title', 'description', 'true_choice', 'false_choice', 'answer', 'marks']
        labels = {
            'question_num': 'Question #',
            'answer': 'Answer is True?',
        }
        widgets = {
            'question_num': NumberInput(attrs={'class': u'form-control','placeholder': u'Enter Question Number'}),
            'title': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Title'}),
            'description': Textarea(attrs={'class': u'form-control','placeholder': u'Enter Description'}),
            'true_choice': TextInput(attrs={'class': u'form-control','placeholder': u'Enter True Choice Description'}),
            'false_choice': TextInput(attrs={'class': u'form-control','placeholder': u'Enter False Choice Description'}),
            'marks': NumberInput(attrs={'class': u'form-control','placeholder': u'Enter Marks'}),
        }


class ResponseQuestionForm(forms.ModelForm):
    class Meta:
        model = ResponseQuestion
        fields = ['question_num', 'title', 'description', 'answer', 'marks']
        labels = {
            'question_num': 'Question #',
        }
        widgets = {
            'question_num': NumberInput(attrs={'class': u'form-control','placeholder': u'Enter Question Number'}),
            'title': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Title'}),
            'description': Textarea(attrs={'class': u'form-control','placeholder': u'Enter Description'}),
            'answer': Textarea(attrs={'class': u'form-control','placeholder': u'Enter Answer'}),
            'marks': NumberInput(attrs={'class': u'form-control','placeholder': u'Enter Marks'}),
    }

QUIZ_QUESTION_TYPE_CHOICES = (
    (settings.TRUEFALSE_QUESTION_TYPE, 'True/False'),
)

class QuizQuestionTypeForm(forms.Form):
    question_num = forms.IntegerField(label='Question #', initial=1, widget=forms.NumberInput(attrs={'class': u'form-control','placeholder': u'Enter Question Number', 'min': '0', 'max': '100', 'step': '1'}))
    question_type = forms.CharField(label='Question Type', widget=forms.Select(attrs={'class': u'form-control'}, choices=QUIZ_QUESTION_TYPE_CHOICES))

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['quiz_num', 'title', 'description', 'start_date', 'due_date', 'worth']
        labels = {
            'quiz_num': 'Quiz #',
            'worth': 'Worth % of Final Mark',
        }
        widgets = {
            'quiz_num': NumberInput(attrs={'class': u'form-control','placeholder': u'Enter Quiz Number'}),
            'title': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Title'}),
            'description': Textarea(attrs={'class': u'form-control','placeholder': u'Enter Description'}),
            'start_date': SelectDateWidget(),
            'due_date': SelectDateWidget(),
            'worth': Select(attrs={'class': u'form-control'}),
        }

EXAM_QUESTION_TYPE_CHOICES = (
    (settings.MULTIPLECHOICE_QUESTION_TYPE, 'Multiple-Choice'),
)

class ExamQuestionTypeForm(forms.Form):
    question_num = forms.IntegerField(label='Question #', initial=1, widget=forms.NumberInput(attrs={'class': u'form-control','placeholder': u'Enter Question Number', 'min': '0', 'max': '100', 'step': '1'}))
    question_type = forms.CharField(label='Question Type', widget=forms.Select(attrs={'class': u'form-control'}, choices=EXAM_QUESTION_TYPE_CHOICES))


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
            'exam_num': NumberInput(attrs={'class': u'form-control','placeholder': u'Enter Exam Number'}),
            'title': TextInput(attrs={'class': u'form-control','placeholder': u'Enter Title'}),
            'description': Textarea(attrs={'class': u'form-control','placeholder': u'Enter Description'}),
            'start_date': SelectDateWidget(),
            'due_date': SelectDateWidget(),
            'worth': Select(attrs={'class': u'form-control'}),
        }
