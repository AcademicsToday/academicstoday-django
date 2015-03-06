from django.contrib import admin

## Special Thanks:
## http://www.djangobook.com/en/2.0/chapter06.html
#
from registrar.models import Course
from registrar.models import Student
from registrar.models import Teacher
from registrar.models import Announcement
from registrar.models import Syllabus

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Announcement)
admin.site.register(Syllabus)
