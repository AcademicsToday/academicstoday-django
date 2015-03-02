from django.core.urlresolvers import resolve
from django.test import TestCase
from landpage.views import landpage

# Create your tests here.
class LandpageTest(TestCase):

    def test_root_url_resolves_to_homep_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func,landpage.load_landpage)