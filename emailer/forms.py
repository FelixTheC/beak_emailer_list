#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 16.09.20
@author: felix
"""
from django.forms import ModelForm
from tinymce.widgets import TinyMCE

from emailer.models import Email
from emailer.models import EmailSignature


class EmailForm(ModelForm):

    class Meta:
        model = Email
        fields = ('subject', 'content', 'kitas', 'representatives')
        widgets = {
            'content': TinyMCE(attrs={'cols': 30, 'rows': 30})
        }


class EmailSignatureForm(ModelForm):
    class Meta:
        model = EmailSignature
        fields = ('text', 'active', )
        widgets = {
            'text': TinyMCE(attrs={'cols': 10, 'rows': 20})
        }
