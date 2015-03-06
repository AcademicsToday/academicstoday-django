from django.conf.urls import patterns, include, url

from . import views

# Import custom views.
from teacher.views import announcement
from teacher.views import syllabus
from teacher.views import policy

urlpatterns = patterns('',
    # Announcement
    url(r'^teacher/course/(\d+)/$', announcement.announcements_page),
    url(r'^teacher/course/(\d+)/home$', announcement.announcements_page),
    url(r'^teacher/course/(\d+)/announcement$', announcement.announcements_page),
    url(r'^teacher/course/(\d+)/new_announcement_modal$', announcement.new_announcement_modal),
    url(r'^teacher/course/(\d+)/save_new_announcement$', announcement.save_new_announcement),
    url(r'^teacher/course/(\d+)/announcement_delete$', announcement.announcement_delete),

    # Syllabus
    url(r'^teacher/course/(\d+)/syllabus$', syllabus.syllabus_page),
    url(r'^teacher/course/(\d+)/syllabus_modal$', syllabus.syllabus_modal),
    url(r'^teacher/course/(\d+)/save_syllabus$', syllabus.save_syllabus),
    url(r'^teacher/course/(\d+)/delete_syllabus$', syllabus.delete_syllabus),                   
 
    # Policy
    url(r'^teacher/course/(\d+)/policy$', policy.policy_page),
    url(r'^teacher/course/(\d+)/policy_modal$', policy.policy_modal),
    url(r'^teacher/course/(\d+)/save_policy$', policy.save_policy),
    url(r'^teacher/course/(\d+)/delete_policy$', policy.delete_policy),
)
