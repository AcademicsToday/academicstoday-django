from django.shortcuts import render
from django.core import serializers
import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required(login_url='/landpage')
def my_publications_page(request):
    return render(request, 'publisher/my_publication/view.html',{
        'user': request.user,
        'tab': 'my_publications',
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS
    })


@login_required()
def my_publications_table(request):
    return render(request, 'publisher/my_publication/table.html',{
        'user': request.user,
        'tab': 'my_publications',
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS
    })
