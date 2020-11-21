#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 21.11.20
@author: felix
"""
from django import forms

from kita_friends.models import KitaFriends


class KitaFriendsForm(forms.ModelForm):
    class Meta:
        model = KitaFriends
        fields = ('first_name', 'name', 'email', 'kita')
        labels = {
            'first_name': '*Vorname',
            'name': '*Name',
            'email': '*E-Mail',
        }
