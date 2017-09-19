# -*- coding: utf-8 -*-
import time
import base64
import hashlib
import pytz
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.signing import Signer
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db.models import Q
from django.utils import crypto
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from shared_foundation import constants


def get_random_string(length=31,
                    allowed_chars='abcdefghijkmnpqrstuvwxyz'
                                       'ABCDEFGHIJKLMNPQRSTUVWXYZ'
                                       '23456789'):
    """
    Random string generator simplified from Django.
    """
    return crypto.get_random_string(length, allowed_chars)


def get_unique_username_from_email(email):
    """
    Uniquely generate our 'username' by taking the email and create a hash.
    Source: https://github.com/dabapps/django-email-as-username/blob/master/emailusernames/utils.py
    """
    email = email.lower()  # Emails should be case-insensitive unique
    converted = email.encode('utf8', 'ignore')  # Deal with internationalized email addresses
    return base64.urlsafe_b64encode(hashlib.sha256(converted).digest())[:30]


def reverse_with_full_domain(reverse_url_id, resolve_url_args=[]):
    """
    Enhanced "reverse" function which will include the HTTP PROTOCAL and HTTP
    DOMAIN for the reversed link.
    """
    url = settings.ACADEMICSTODAY_APP_HTTP_PROTOCOL
    url += settings.ACADEMICSTODAY_APP_HTTP_DOMAIN
    url += reverse(reverse_url_id, args=resolve_url_args)
    url = url.replace("None","en")
    return url


def django_sign(plaintext_value, salt_value=None):
    """
    Function will take the plaintext value and sign with the django SECRET_KEY.
    """
    # Convert our User's ID into an encrypted value.
    # Note: https://docs.djangoproject.com/en/dev/topics/signing/
    signer = Signer(salt=salt_value)
    return signer.sign(plaintext_value)


def django_unsign(signed_value, salt_value=None):
    """
    Function will take the signed value and get the plaintext value by cheching
    this django SECRET_KEY.
    """
    try:
        # Convert our signed value into a text.
        signer = Signer(salt=salt_value)
        return signer.unsign(signed_value)
    except Exception as e:
        return None


def is_email_unique(email):
    """
    Utility function checks to see if parameter email is unique or not.
    """
    return not User.objects.filter(email=email).exists()


def generate_hash():
    """
    Utility function generate will generate a hash on a timestamp.
    """
    hash = hashlib.sha1()
    time_str = str(time.time())
    utf8_time_str = time_str.encode('utf-8')
    hash.update(utf8_time_str)
    return  hash.hexdigest()
