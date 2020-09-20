#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 20.09.20
@author: felix
"""
from django.core.exceptions import ValidationError
from django.test import TestCase

from kita.models import Kita


class KitaTest(TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        Kita.objects.all().delete()

    def test_create_kita(self):
        obj = Kita(name='Kita',
                   street_name='Foobar',
                   number=12,
                   postal_code=12345,
                   email='info@kita.de')
        obj.save()
        obj.refresh_from_db()
        self.assertIsNotNone(obj)

    def test_postalcode_invalid_lt_10000(self):
        try:
            Kita(name='Kita',
                 street_name='Foobar',
                 number=12,
                 postal_code=9999,
                 email='info@kita.de')
        except ValidationError:
            pass

    def test_postalcode_invalid_gt_99999(self):
        try:
            Kita(name='Kita',
                 street_name='Foobar',
                 number=12,
                 postal_code=100000,
                 email='info@kita.de')
        except ValidationError:
            pass

    def test_postalcode_invalid_str(self):
        try:
            Kita(name='Kita',
                 street_name='Foobar',
                 number=12,
                 postal_code='12345',
                 email='info@kita.de')
        except ValidationError:
            pass
