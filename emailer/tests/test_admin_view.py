#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@created: 03.09.20
@author: felix
"""
from django.contrib import messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.core import mail
from django.test import override_settings
from django.urls import reverse

from emailer.models import Email
from emailer.models import EmailSignature
from kita.models import Kita
from kita_representative.models import KitaRepresentative
from test_utils.base_test import BaseTest


class AdminViewTest(BaseTest):

    @staticmethod
    def create_dummy_data():
        obj = Kita(name='Kita',
                   street_name='Foobar',
                   number=12,
                   postal_code=12345,
                   email='info@kita.de')
        obj.save()
        KitaRepresentative(first_name='Jon',
                           name='Doe',
                           email='jondoe@test.com',
                           kita=obj
                           ).save()
        KitaRepresentative(first_name='Jane',
                           name='Doe',
                           email='janedoe@test.com',
                           kita=obj
                           ).save()

    def tearDown(self) -> None:
        super().tearDown()
        Kita.objects.all().delete()
        KitaRepresentative.objects.all().delete()
        Email.objects.all().delete()
        EmailSignature.objects.all().delete()

    @staticmethod
    def create_test_email(subject='Test email'):
        sign = EmailSignature(text='Best regards\nJon Doe', active=True)
        sign.save()
        obj = Email(subject='Test',
                    content='Some text',
                    greeting=sign)
        obj.save()
        for k_obj in Kita.objects.all():
            obj.kitas.add(k_obj)
        for kp_obj in KitaRepresentative.objects.all():
            obj.representatives.add(kp_obj)
        obj.save()

    def test_access_admin(self):
        resp = self.client.get('/admin/', follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_parents_on_admin(self):
        resp = self.client.get('/admin/emailer', follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_admin_info_view(self):
        resp = self.client.get('/admin/emailer/email', follow=True)
        self.assertContains(resp, f'{Email.objects.count()} emails')

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_admin_view_contains_send_email_function(self):
        self.create_dummy_data()
        self.create_test_email()

        change_url = reverse('admin:emailer_email_changelist')

        resp = self.client.get(change_url, follow=True)

        self.assertContains(resp, 'Delete selected emails')
        self.assertContains(resp, 'Send selected email')

        self.client.post(change_url, data={
            'action': 'send_emails',
            ACTION_CHECKBOX_NAME: [Email.objects.first().pk, ],
        }, follow=True)

        total_emails = Kita.objects.count() + KitaRepresentative.objects.count()
        self.assertEqual(len(mail.outbox), total_emails)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_admin_view_contains_send_email_only_one_allowed(self):
        self.create_dummy_data()
        self.create_test_email()
        self.create_test_email(subject='Another test email')

        change_url = reverse('admin:emailer_email_changelist')

        resp = self.client.get(change_url, follow=True)

        self.assertContains(resp, 'Delete selected emails')
        self.assertContains(resp, 'Send selected email')

        self.client.post(change_url, data={
            'action': 'send_emails',
            ACTION_CHECKBOX_NAME: [obj.pk for obj in Email.objects.all()],
        }, follow=True)

        self.assertEqual(len(mail.outbox), 0)
