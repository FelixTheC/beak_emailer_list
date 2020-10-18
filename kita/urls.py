#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 18.10.20
@author: felix
"""
from django.urls import path

from kita.views import KitaCRUDView

urlpatterns = [
    path('', KitaCRUDView.as_view(), name='crud_kita'),
]

