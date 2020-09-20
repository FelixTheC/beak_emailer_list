#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 03.09.20
@author: felix
"""
from django.contrib.auth.models import User
from django.test import TestCase


class BaseTest(TestCase):
    username = 'TestUser'
    passwd = 'password_1234'

    def create_user(self):
        obj, _ = User.objects.update_or_create(username=self.username,
                                               password=self.passwd,
                                               is_superuser=True,
                                               is_staff=True,
                                               is_active=True)
        obj.set_password(self.passwd)
        obj.save()

    def setUp(self) -> None:
        self.create_user()
        if not self.client.login(username=self.username, password=self.passwd):
            raise RuntimeError

    def tearDown(self) -> None:
        if self.client:
            self.client.logout()
