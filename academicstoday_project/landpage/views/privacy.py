import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings


def privacy_page(request):
    return render(request, 'offlandpage/page/privacy.html',{
        'tab': 'privacy',
        'local_css_urls': ["css/offlandpage.css",
                            "bower_components/bootstrap/dist/css/bootstrap.min.css"],
        'local_js_urls': ["bower_components/jquery/dist/jquery.min.js",
                           "bower_components/bootstrap/dist/js/bootstrap.min.js",],
    })
