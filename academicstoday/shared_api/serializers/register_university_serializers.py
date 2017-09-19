from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from shared_foundation import models
from shared_foundation import utils


class RegisterUniversitySerializer(serializers.Serializer):
    schema_name = serializers.CharField(
        allow_blank=False,
        max_length=255,
        trim_whitespace=True
    )
    name = serializers.CharField(
        allow_blank=False,
        max_length=255,
        trim_whitespace=True
    )
    alternate_name = serializers.CharField(
        allow_blank=False,
        max_length=255,
        trim_whitespace=True
    )

    def validate(self, attrs):
        schema_name = attrs.get('schema_name')

        if models.SharedUniversity.objects.filter(schema_name=schema_name).exists():
            raise serializers.ValidationError(_("Schema_name is not unique."))

        return attrs
