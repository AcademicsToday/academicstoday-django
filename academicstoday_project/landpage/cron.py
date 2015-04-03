from django_cron import CronJobBase, Schedule
from django.conf import settings
from account.models import Student
from registrar.models import Course
from landpage.models import LandpageTopPickCourse

class TopCoursesPickingCronJob(CronJobBase):
    RUN_EVERY_MINS = 0 # every 2 hours (value=120)
    
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'landpage.top_courses_cron_job'    # a unique code
    
    def do(self):
        """
            Function will iterate through all the courses in the database and
            check how many students are enrolled in them. The courses with the
            top enrollment count will be set as top courses.
        """
        # Get all the courses in our database.
        course_list = Course.objects.filter(status=settings.COURSE_AVAILABLE_STATUS)
        
        # Make list on course_id and count.
        courses = {}
        for course in course_list:
            count = course.students.count()
            courses[course.id] = count

        # Arrange the biggest to smallest.
        sorted(courses.values())

        # Delete all old entries
        try:
            LandpageTopPickCourse.objects.all().delete()
        except LandpageTopPickCourse.DoesNotExist:
            pass

        # Pick the top three courses and create our entries here
        index = 1
        max_count = 2
        for course_id in courses.keys():
            if index < max_count:
                course_obj = Course.objects.get(id=course_id)
                LandpageTopPickCourse.objects.create(
                   id=index,
                   course=course_obj,
                )
            index += 1
