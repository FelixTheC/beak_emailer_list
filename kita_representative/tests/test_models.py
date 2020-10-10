#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 16.09.20
@author: felix
"""
from django.core import mail
from django.test import TestCase
from django.test import override_settings

from kita.models import Kita
from kita_representative.models import KitaRepresentative


class KitaRepresentativeTest(TestCase):

    def setUp(self) -> None:
        Kita(name='Test',
             street_name='abcdefghijk',
             number='12a',
             postal_code=12345,
             email='test@test.com').save()

    def tearDown(self) -> None:
        Kita.objects.all().delete()
        KitaRepresentative.objects.all().delete()

    def test_create_one_representatives(self):
        obj = KitaRepresentative(first_name='Jon',
                                 name='Doe',
                                 email='jondoe@test.com',
                                 kita=Kita.objects.get(name='Test')
                                 )
        obj.save()
        obj.refresh_from_db()
        self.assertIsNotNone(obj)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_too_many_respresentatives(self):
        KitaRepresentative(first_name='Jon',
                           name='Doe',
                           email='jondoe@test.com',
                           kita=Kita.objects.get(name='Test')
                           ).save()
        KitaRepresentative(first_name='Jane',
                           name='Doe',
                           email='janedoe@test.com',
                           kita=Kita.objects.get(name='Test')
                           ).save()
        KitaRepresentative(first_name='Jim',
                           name='Doe',
                           email='jimdoe@test.com',
                           kita=Kita.objects.get(name='Test')
                           ).save()

        self.assertEqual(len(mail.outbox), 1)
