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
from registrar.models import PeerReview
from publisher.views import publication


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class PublicationTestCase(TestCase):
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

    def test_url_resolves_to_publication_page_view(self):
        found = resolve('/publication/1')
        self.assertEqual(found.func, publication.publication_page)

    def test_publication_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/publication/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'/publish',response.content)
        self.assertIn(b'Publication #',response.content)

    def test_url_resolves_to_peer_review_modal_view(self):
        found = resolve('/publication/1/peer_review_modal')
        self.assertEqual(found.func, publication.peer_review_modal)
    
    def test_peer_review_modal_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = client.post('/publication/1/peer_review_modal',{
            'peer_review_id': 0
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ajax_save_peer_review(0);',response.content)

    def test_url_resolves_to_save_peer_review_view(self):
        found = resolve('/publication/1/save_peer_review')
        self.assertEqual(found.func, publication.save_peer_review)
    
    def test_save_peer_review_returns_correct_html(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        
        # Insert
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

        
        # Add peer review
        publications = Publication.objects.all()
        publication_id = publications[0].publication_id
        response = client.post('/publication/'+str(publication_id)+'/save_peer_review', {
            'peer_review_id':0,
            'marks': 5,
             'text': 'Excellent!',
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'submitted')


    def test_url_resolves_to_delete_peer_review_view(self):
        found = resolve('/publication/'+str(1)+'/delete_peer_review')
        self.assertEqual(found.func, publication.delete_peer_review)
    
    def test_delete_publication_returns_correct_html(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
            
        # Insert Publication
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
                
        # Add peer review
        publications = Publication.objects.all()
        publication_id = publications[0].publication_id
        response = client.post('/publication/'+str(publication_id)+'/save_peer_review', {
            'peer_review_id':0,
            'marks': 5,
            'text': 'Excellent!',
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'submitted')

        # Add peer review
        reviews = PeerReview.objects.all()
        review_id = reviews[0].review_id
        response = client.post('/publication/'+str(publication_id)+'/delete_peer_review', {
            'peer_review_id':review_id,
        }, **kwargs)
        self.assertEqual(response.status_code, 200)
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array['status'], 'success')
        self.assertEqual(array['message'], 'deleted')

