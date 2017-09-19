# -*- coding: utf-8 -*-
from django.shortcuts import render
from shared_foundation.models import SharedUniversity

def master_page(request):
    universities = SharedUniversity.objects.all()
    return render(request, 'shared_dashboard/master_view.html',{
        'current_page': 'home-master',
        'universities': universities
    })
