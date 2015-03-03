from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from . import views
import json
from landpage.models import LandpageTeamMember
from landpage.models import LandpageCoursePreview
from landpage.models import CoursePreview


# Create your tests here.
class LandpageTest(TestCase):
    def setUp(self):
        CoursePreview.objects.create(
            image_filename="roundicons.png",
            title="Comics Book Course",
            sub_title="The definitive course on comics!",
            category="",
            description="",
            summary="",
        )

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func,views.landpage_page)

    def test_robots_txt_page(self):
        found = resolve('/robots.txt');
        self.assertEqual(found.func,views.robots_txt_page)

    def test_humans_txt_page(self):
        found = resolve('/humans.txt');
        self.assertEqual(found.func,views.humans_txt_page)

    def test_landpage_page(self):
        found = resolve('/landpage');
        self.assertEqual(found.func,views.landpage_page)

# Example of using HttpRequest
#    def test_course_preview_returns_corret_html(self):
#        request = HttpRequest()
#        request.POST = QueryDict('course_preview_id=1')
#        response = views.course_preview_modal(request)
#
#        # Validate
#        print(response.content)
#        self.assertIn(b'<form',response.content)

    def test_course_preview_modal_returns_correct_html(self):
        parameters = {"course_preview_id":1}
        client = Client()
        response = client.post(
            '/course_preview_modal',
            data=parameters,
        )
        self.assertIn(b'Comics Book Course',response.content)
        self.assertIn(b'The definitive course on comics!',response.content)

    def test_login_modal_returns_correct_html(self):
        client = Client()
        response = client.post('/login_modal')
        self.assertTrue(response.content.startswith(b'<div'))
        self.assertIn(b'login_modal',response.content)
        self.assertIn(b'loginForm',response.content)

    def test_register_modal_returns_correct_html(self):
        client = Client()
        response = client.post('/register_modal')
        self.assertTrue(response.content.startswith(b'<div'))
        self.assertIn(b'register_modal',response.content)
        self.assertIn(b'register_form',response.content)
