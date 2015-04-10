from django.shortcuts import render
from django.core import serializers
import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required(login_url='/landpage')
def catalog_page(request):
    return render(request, 'publisher/catalog/view.html',{
        'user': request.user,
        'tab': 'publisher_catalog',
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS
    })


@login_required()
def certificates_table(request):
    return render(request, 'publisher/catalog/table.html',{
        'user': request.user,
        'tab': 'certificates',
        'local_css_urls': settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls': settings.SB_ADMIN_2_JS_LIBRARY_URLS
    })
