#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 05.10.20
@author: felix
"""
from django import forms

from kita_representative.models import KitaRepresentative


class KitaRepresentativeForm(forms.ModelForm):
    class Meta:
        model = KitaRepresentative
        fields = ('first_name', 'name', 'email', 'kita')
        labels = {
            'first_name': 'Vorname',
            'name': 'Name',
            'email': 'E-Mail',
        }
