from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from account.models import Student
from registrar.models import Course
from landpage.models import LandpageTopPickCourse

class Command(BaseCommand):
    help = 'Picks the top 9 courses with the highest student enrollment.'
    
    def handle(self, *args, **options):
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
        max_count = 4
        for course_id in courses.keys():
            if index < max_count:  # Pick top 3 courses.
                course_obj = Course.objects.get(id=course_id)
                LandpageTopPickCourse.objects.create(
                    id=index,
                    course=course_obj,
                )
            index += 1