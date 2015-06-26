import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings


def login_modal(request):
    return render(request, 'landpage/login/modal.html',{})