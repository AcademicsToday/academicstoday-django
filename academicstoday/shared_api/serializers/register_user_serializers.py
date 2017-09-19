from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from shared_foundation import models
from shared_foundation import utils


class RegisterUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        allow_blank=False,
        max_length=64,
        trim_whitespace=True
    )
    last_name = serializers.CharField(
        allow_blank=False,
        max_length=64,
        trim_whitespace=True
    )
    email = serializers.EmailField(
        allow_blank=False,
        max_length=64,
        trim_whitespace=True
    )
    password = serializers.CharField(
        allow_blank=False,
        max_length=64,
        trim_whitespace=True
    )
    password_repeated = serializers.CharField(
        allow_blank=False,
        max_length=64,
        trim_whitespace=True
    )

    def validate(self, attrs):
        password = attrs.get('password')
        password_repeated = attrs.get('password_repeated')

        if password != password_repeated:
            raise serializers.ValidationError("Passwords do not match.")

        return attrs
