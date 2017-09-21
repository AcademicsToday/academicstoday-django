# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from shared_foundation.models import SharedUniversity


@login_required(login_url='/en/login')
def master_page(request):
    return render(request, 'tenant_registrar/master_view.html',{
        'current_page': 'home-master',
    })


@login_required(login_url='/en/login')
def detail_page(request):
    return render(request, 'tenant_registrar/master_view.html',{
        'current_page': 'home-master',
    })


@login_required(login_url='/en/login')
def closed_page(request):
    return render(request, 'tenant_registrar/closed_view.html',{
        'current_page': 'home-master',
    })
