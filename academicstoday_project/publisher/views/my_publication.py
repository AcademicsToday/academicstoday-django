from django.shortcuts import render
from django.core import serializers
import json
import datetime
import os
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from publisher.models import Publication
from registrar.models import PeerReview
from publisher.forms import PublicationForm

@login_required(login_url='/landpage')
def my_publications_page(request):
    try:
        publications = Publication.objects.filter(author=request.user)
    except Publication.DoesNotExist:
        publications = None
    return render(request, 'publisher/my_publication/view.html',{
        'publications': publications,
        'user': request.user,
        'tab': 'my_publications',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS
    })


@login_required()
def refresh_publications_table(request):
    try:
        publications = Publication.objects.filter(author=request.user)
    except Publication.DoesNotExist:
        publications = None
    return render(request, 'publisher/my_publication/table.html',{
        'publications': publications,
        'user': request.user,
        'tab': 'my_publications',
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS
    })


@login_required()
def my_publication_modal(request):
    if request.method == u'POST':
        form = None
        publication_id = int(request.POST['publication_id'])
        if publication_id > 0:
            upload = Publication.objects.get(publication_id=publication_id)
            form = PublicationForm(instance=upload)
        else:
            form = PublicationForm()
        return render(request, 'publisher/my_publication/modal.html',{
            'form': form,
        })



@login_required()
def save_publication(request):
    response_data = {'status' : 'failed', 'message' : 'unknown error with saving'}
    if request.is_ajax():
        if request.method == 'POST':
            publication_id = int(request.POST['publication_id'])
            form = PublicationForm(request.POST, request.FILES)
            
            # If publication already exists, then delete local file.
            if publication_id > 0:
                # Delete previous file.
                try:
                    upload = Publication.objects.get(publication_id=publication_id)
                except Publication.DoesNotExist:
                    return HttpResponse(json.dumps({
                        'status' : 'failed', 'message' : 'record does not exist'
                    }), content_type="application/json")
                
                if upload.file:
                    if os.path.isfile(upload.file.path):
                        os.remove(upload.file.path)
                        upload.file = None
                        upload.save()
                form.instance = upload
    
        # Save if valid
        form.instance.author = request.user
        if form.is_valid():
            form.save()
            response_data = {'status' : 'success', 'message' : 'saved'}
        else:
            response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def delete_publication(request):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deleting'}
    if request.is_ajax():
        if request.method == 'POST':
            publication_id = int(request.POST['publication_id'])
            try:
                publication = Publication.objects.get(publication_id=publication_id)
                for peer_review in publication.reviews.all():
                    peer_review.delete()
                publication.delete()
                response_data = {'status' : 'success', 'message' : 'deleted'}
            except Publication.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'record not found'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
