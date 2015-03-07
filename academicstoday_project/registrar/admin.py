from django.contrib import admin

## Special Thanks:
## http://www.djangobook.com/en/2.0/chapter06.html
#
from registrar.models import Course
from registrar.models import Student
from registrar.models import Teacher
from registrar.models import Announcement
from registrar.models import Syllabus
from registrar.models import Lecture
from registrar.models import Assignment
from registrar.models import EssayQuestion
from registrar.models import MultipleChoiceQuestion
from registrar.models import TrueFalseQuestion
from registrar.models import ResponseQuestion

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Announcement)
admin.site.register(Syllabus)
admin.site.register(Lecture)
admin.site.register(Assignment)
admin.site.register(EssayQuestion)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(TrueFalseQuestion)
admin.site.register(ResponseQuestion)
