# -*- coding: utf-8 -*-
from django.shortcuts import render
from shared_foundation.models import SharedUniversity


def create_master_page(request):
    return render(request, 'shared_university/create/master_view.html',{
        'current_page': 'home-master',
    })


def create_detail_page(request):
    return render(request, 'shared_university/create/detail_view.html',{
        'current_page': 'home-master',
    })
