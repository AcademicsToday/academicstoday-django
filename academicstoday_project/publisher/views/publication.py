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


@login_required(login_url='/landpage')
def publication_page(request, publication_id):
    try:
        publication = Publication.objects.get(publication_id=publication_id)
    except Publication.DoesNotExist:
        publication = None
    return render(request, 'publisher/publication/view.html',{
        'publication': publication,
        'user': request.user,
        'tab': 'publisher_catalog',
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS
    })
