from django.conf.urls import patterns, include, url

from . import views

# Import custom views.
from teacher.views import announcement

urlpatterns = patterns('',
    # Announcement
    url(r'^teacher/course/(\d+)/$', announcement.announcements_page),
    url(r'^teacher/course/(\d+)/home$', announcement.announcements_page),
    url(r'^teacher/course/(\d+)/announcement$', announcement.announcements_page),
    url(r'^teacher/course/(\d+)/new_announcement_modal$', announcement.new_announcement_modal),
    url(r'^teacher/course/(\d+)/save_new_announcement$', announcement.save_new_announcement),
    url(r'^teacher/course/(\d+)/announcement_delete$', announcement.announcement_delete),

)
