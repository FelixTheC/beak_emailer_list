#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 18.04.21
@author: felix
"""
from unittest import TestCase

from django.db.utils import IntegrityError
from scheduler.models import ScheduleCommander
import ujson


class ScheduleModelTest(TestCase):

    def test_create_command_execution_date_required(self):
        self.assertRaises(IntegrityError, ScheduleCommander.objects.create,
                          module='some_module.utils',
                          func='main',
                          args=str(tuple()),
                          kwargs=ujson.dumps({})
                          )
