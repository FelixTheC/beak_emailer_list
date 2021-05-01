#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 01.05.21
@author: felix
"""
from django.db import models


class BigPrimaryKeyModel(models.Model):
    id = models.BigIntegerField(primary_key=True, db_index=True)

    class Meta:
        abstract = True


class UUIDPrimaryKeyModel(models.Model):
    id = models.UUIDField(primary_key=True, db_index=True)

    class Meta:
        abstract = True
