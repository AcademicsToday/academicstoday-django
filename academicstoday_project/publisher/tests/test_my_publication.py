from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static, settings
import json
from publisher.models import Publication
from publisher.views import my_publication


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class MyPublicationTestCase(TestCase):
    def tearDown(self):
        publications = Publication.objects.all()
        for publication in publications:
            publication.delete()
        User.objects.get(email=TEST_USER_EMAIL).delete()
    
    def setUp(self):
        # Create our user.
        User.objects.create_user(
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user = User.objects.get(email=TEST_USER_EMAIL)


    def test_url_resolves_to_catalog_page_view(self):
        found = resolve('/my_publications')
        self.assertEqual(found.func, my_publication.my_publications_page)


    def test_catalog_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/my_publications')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'/publish',response.content)
        self.assertIn(b'Catalog',response.content)

    def test_url_resolves_to_refresh_publications_table_view(self):
        found = resolve('/refresh_publications_table')
        self.assertEqual(found.func, my_publication.refresh_publications_table)
    
    def test_certificate_table_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/refresh_publications_table')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'popup_publication_modal(0);',response.content)

    def test_url_resolves_to_my_publication_modal_view(self):
        found = resolve('/my_publication_modal')
        self.assertEqual(found.func, my_publication.my_publication_modal)
    
    def test_my_publication_modal_returns_correct_html(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/my_publication_modal', {'publication_id':0,}, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ajax_create_publication',response.content)

    def test_url_resolves_to_save_publication_view(self):
        found = resolve('/save_publication')
        self.assertEqual(found.func, my_publication.save_publication)
    
    def test_save_publication_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        file_path = settings.MEDIA_ROOT + '/sample.pdf'
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/save_publication',{
                'publication_id': 0,
                'title': 'test',
                'description': 'test',
                'file': fp
            }, **kwargs)
            self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'saved')

    def test_save_publication_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        file_path = settings.MEDIA_ROOT + '/sample.pdf'
        
        # Insert
        with open(file_path, 'rb') as fp:
            self.assertTrue(fp is not None)
            response = client.post('/save_publication',{
                'publication_id': 0,
                'title': 'test',
                'description': 'test',
                'file': fp
            }, **kwargs)
            self.assertEqual(response.status_code, 200)
        
        # Delete
        response = client.post('/delete_publication',{
            'publication_id': 1,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'deleted')
