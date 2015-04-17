from django.contrib import admin
from landpage.models import LandpageTeamMember
from landpage.models import LandpageCoursePreview
from landpage.models import LandpageTopPickCourse
from landpage.models import CoursePreview
from landpage.models import LandpageContactMessage
from landpage.models import LandpagePartner

admin.site.register(LandpageTeamMember)
admin.site.register(LandpageCoursePreview)
admin.site.register(LandpageTopPickCourse)
admin.site.register(CoursePreview)
admin.site.register(LandpageContactMessage)
admin.site.register(LandpagePartner)