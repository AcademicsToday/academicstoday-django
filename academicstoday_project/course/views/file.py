from django.shortcuts import render
from django.http import HttpResponse

def load_robots_txt(request):
    return render(request, 'misc/robots.txt', {}, content_type="text/plain")

def load_humans_txt(request):
    return render(request, 'misc/humans.txt', {}, content_type="text/plain")
