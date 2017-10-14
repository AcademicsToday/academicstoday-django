# -*- coding: utf-8 -*-
from django.shortcuts import render
from shared_foundation.models import SharedUniversity


def create_master_page(request):
    return render(request, 'shared_university/create/master_view.html',{
        'page_id': 'shared-university-create',
    })


def create_detail_page(request):
    return render(request, 'shared_university/create/detail_view.html',{
        'page_id': 'shared-university-create',
    })


def launchpad_master_page(request):
    return render(request, 'shared_university/create/master_view.html',{
        'page_id': 'home-master',
    })


def list_master_page(request):
    return render(request, 'shared_university/list/master_view.html',{
        'page_id': 'shared-university-list',
        'universities': SharedUniversity.objects.all()
    })
