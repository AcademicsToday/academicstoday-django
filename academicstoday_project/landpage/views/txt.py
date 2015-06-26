import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings


def robots_txt_page(request):
    return render(request, 'misc/robots.txt', {}, content_type="text/plain")


def humans_txt_page(request):
    return render(request, 'misc/humans.txt', {}, content_type="text/plain")


def terms_txt_page(request):
    return render(request, 'misc/terms.txt', {}, content_type="text/plain")


def privacy_txt_page(request):
    return render(request, 'misc/privacy.txt', {}, content_type="text/plain")