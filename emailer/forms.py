#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 16.09.20
@author: felix
"""
from django.forms import ModelForm

from emailer.models import Email


class EmailForm(ModelForm):

    class Meta:
        model = Email
        fields = ('subject', 'content', 'kitas', 'representatives')
