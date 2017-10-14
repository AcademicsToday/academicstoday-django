# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from shared_foundation.models import SharedUniversity
from tenant_registrar.decorators import tenant_registration_required


@login_required(login_url='/en/login')
@tenant_registration_required
def admin_master_page(request):
    return render(request, 'tenant_dashboard/admin/master_view.html',{
        'page_id': 'tenant_dashboard',
    })


@login_required(login_url='/en/login')
@tenant_registration_required
def teacher_master_page(request):
    return render(request, 'tenant_dashboard/teacher/master_view.html',{
        'page_id': 'tenant_dashboard',
    })


@login_required(login_url='/en/login')
@tenant_registration_required
def student_master_page(request):
    return render(request, 'tenant_dashboard/student/master_view.html',{
        'page_id': 'tenant_dashboard',
    })
