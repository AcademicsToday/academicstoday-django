# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from shared_foundation.models import SharedUniversity
from tenant_registrar.decorators import tenant_registration_required


@login_required(login_url='/en/login')
@tenant_registration_required
def launchpad_master_page(request):
    return render(request, 'shared_index/master_view.html',{
        'current_page': 'home-master',
    })
