from rq import get_current_job
from django_rq import job
from django.core.management import call_command


@job
def send_user_activation_email_func(email):
    call_command('send_user_activation_email', email, verbosity=0, interactive=False)
