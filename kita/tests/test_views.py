#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 18.10.20
@author: felix
"""
import json

from django.test import TestCase

from kita.models import Kita


class KitaViewTest(TestCase):
    test_data = '[{"id":"4","name":"Tagespflege-Jana-Kuenzel","email":"jana.kuenzel@ba-mh.berlin.de","street":"",' \
                '"number":"","postal_code":"","created_at":"2020-03-07 17:12:48","updated":"2020-03-07 17:12:48"},' \
                ' {"id":"5","name":"maerchenhaus2015","email":"maerchenhaus2015@gmail.com","street":null,' \
                '"number":null,"postal_code":null,"created_at":"2020-03-07 19:29:07","updated":"2020-03-07 19:29:07"}]'

    def test_json_post(self):
        resp = self.client.post('/kita/', data={'data': json.loads(self.test_data)},
                                content_type='application/json', secure=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Kita.objects.get(name='Tagespflege-Jana-Kuenzel'))
        self.assertTrue(Kita.objects.get(name='maerchenhaus2015'))
