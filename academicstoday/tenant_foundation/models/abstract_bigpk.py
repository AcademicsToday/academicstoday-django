# -*- coding: utf-8 -*-
from django.db import models


class AbstractBigPk(models.Model):
    """
    Astract class is responsible for overriding the default "id" field which
    gets assigned by Django as "AutoField" to be using the "BigAutoField".
    """

    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True
