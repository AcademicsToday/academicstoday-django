from rq import get_current_job
from django_rq import job
from django.core.management import call_command


@job
def found_university_func(data_dict):
    call_command(
        'found_university',
        data_dict['user_pk'],
        data_dict['schema_name'],
        data_dict['name'],
        data_dict['alternate_name'],
        verbosity=0,
        interactive=False)
