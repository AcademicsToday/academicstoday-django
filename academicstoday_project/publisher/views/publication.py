from django.shortcuts import render
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
from publisher.models import Publication
from registrar.models import PeerReview
from student.forms import PeerReviewForm


@login_required(login_url='/landpage')
def publication_page(request, publication_id):
    try:
        publication = Publication.objects.get(publication_id=publication_id)
    except Publication.DoesNotExist:
        publication = None
    try:
        peer_review = PeerReview.objects.get(user=request.user)
    except PeerReview.DoesNotExist:
        peer_review = None
    return render(request, 'publisher/publication/view.html',{
        'publication': publication,
        'user_review': peer_review,
        'user': request.user,
        'tab': 'publisher_catalog',
        'HAS_ADVERTISMENT': settings.APPLICATION_HAS_ADVERTISMENT,
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS
    })


@login_required()
def peer_review_modal(request, publication_id):
    response_data = {'status' : 'failed', 'message' : 'unknown error with deleting'}
    if request.is_ajax():
        if request.method == 'POST':
            try:
                publication = Publication.objects.get(publication_id=publication_id)
            except Publication.DoesNotExist:
                publication = None
            form = PeerReviewForm()
            return render(request, 'publisher/publication/modal.html',{
                'publication': publication,
                'form': form,
                'user': request.user,
                'tab': 'publisher_catalog',
            })

@login_required()
def save_peer_review(request, publication_id):
    if request.is_ajax():
        if request.method == 'POST':
            peer_review_id = int(request.POST['peer_review_id'])
            form = PeerReviewForm(request.POST, request.FILES);
            
            try:
                publication = Publication.objects.get(publication_id=publication_id)
            except Publication.DoesNotExist:
                return HttpResponse(json.dumps({
                    'status' : 'failed', 'message' : 'record does not exist'
                }), content_type="application/json")
        
            if form.is_valid():
                # Save the peer review
                form.instance.user = request.user
                form.save()
                
                if peer_review_id == 0:
                    publication.reviews.add(form.instance)

                # Indicate success
                response_data = {'status' : 'success', 'message' : 'submitted'}
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def delete_peer_review(request, publication_id):
    response_data = {'status' : 'failed', 'message' : 'unknown deletion error'}
    if request.is_ajax():
        if request.method == 'POST':
            review_id = request.POST['peer_review_id']
            try:
                PeerReview.objects.get(review_id=review_id).delete()
                response_data = {'status' : 'success', 'message' : 'deleted'}
            except PeerReview.DoesNotExist:
                response_data = {'status' : 'failed', 'message' : 'record does not exist'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
