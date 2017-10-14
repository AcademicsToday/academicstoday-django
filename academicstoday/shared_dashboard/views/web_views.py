# -*- coding: utf-8 -*-
from django.db.models import Q
from django.shortcuts import render
from shared_foundation.models import SharedUniversity


def master_page(request):
    # Fetch all the univeristies in our system which are publicaly listed.
    universities = SharedUniversity.objects.filter(
        ~Q(schema_name='public') &
        Q(is_listed=True)
    )

    # Fetch all the universities that I am administrating in.
    my_managing_univerisites = SharedUniversity.objects.filter(
        ~Q(schema_name='public') &
        Q(administrators__id=request.user.id)
    )

    # Fetch all the universities I am teaching at.
    my_teaching_univerisites = SharedUniversity.objects.filter(
        ~Q(schema_name='public') &
        Q(teachers__id=request.user.id)
    )

    # Fetch all the univeristies I am attending as a student.
    my_attending_univerisites = SharedUniversity.objects.filter(
        ~Q(schema_name='public') &
        Q(students__id=request.user.id)
    )
    return render(request, 'shared_dashboard/master_view.html',{
        'page_id': 'shared-dashboard-master',
        'universities': universities,
        'my_managing_univerisites': my_managing_univerisites,
        'my_teaching_univerisites': my_teaching_univerisites,
        'my_attending_univerisites': my_attending_univerisites
    })
