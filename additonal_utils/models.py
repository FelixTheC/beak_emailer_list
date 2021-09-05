#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 01.05.21
@author: felix
"""
import uuid

from django.db import models
from django.db.models import BigAutoField


class BigPrimaryKeyModel(models.Model):
    # id = models.BigIntegerField(primary_key=True, db_index=True, default=BigAutoField)

    class Meta:
        abstract = True


class UUIDPrimaryKeyModel(models.Model):
    id = models.UUIDField(primary_key=True, db_index=True, null=True, blank=True, default=uuid.uuid4)

    class Meta:
        abstract = True