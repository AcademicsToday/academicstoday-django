from django.shortcuts import render
from django.core import serializers
import json
from django.http import HttpResponse
from django.conf import settings


def google_verify_page(request):
    return render(request, 'misc/google.html',{})