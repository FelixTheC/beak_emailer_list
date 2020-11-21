#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 21.11.20
@author: felix
"""
from django.urls import path

from kita_friends.views import AssignFriendToEmailer

urlpatterns = [
    path('assign_newsletter/', AssignFriendToEmailer.as_view(), name='assign_friend_to_emailer'),
]
