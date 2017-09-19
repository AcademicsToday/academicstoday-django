# -*- coding: utf-8 -*-
from django.shortcuts import render
from shared_foundation.models import SharedUniversity


def master_page(request):
    print(request.user)
    return render(request, 'tenant_dashboard/master_view.html',{
        'current_page': 'home-master',
    })
