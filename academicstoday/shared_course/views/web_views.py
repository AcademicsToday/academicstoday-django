# -*- coding: utf-8 -*-
from django.db.models import Q
from django.shortcuts import render
from shared_foundation.models import SharedUniversity


def master_page(request):
    return render(request, 'shared_course/master_view.html',{
        'page_id': 'shared_course',
    })


def detail_page(request, course_pk=None):
    return render(request, 'shared_course/detail_view.html',{
        'page_id': 'shared_course',
    })
