#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 05.10.20
@author: felix
"""
from django.urls import path

from kita_representative.views import AssignToEmailer

urlpatterns = [
    path('assign_newsletter/', AssignToEmailer.as_view(), name='assign_to_emailer'),
]
