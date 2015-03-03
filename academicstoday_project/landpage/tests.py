from django.core.urlresolvers import resolve
from django.test import TestCase
from . import views

# Create your tests here.
class LandpageTest(TestCase):

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
