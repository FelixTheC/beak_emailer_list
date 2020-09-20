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
from test_utils.base_test import BaseTest


class AdminViewTest(BaseTest):

    @staticmethod
    def create_parents():
        Parent.objects.create(
            first_name='Jon',
            last_name='Doe',
            child_name='Jon jr.',
            email='jondoe@test.com'
        )
        Parent.objects.create(
            first_name='Jane',
            middle_name='Foo',
            last_name='Bar',
            child_name='Mini Me',
            email='foobar@test.com',
            mobil='0123456789'
        )

    @staticmethod
    def create_test_email(subject='Test email'):
        obj = Email.objects.create(
            subject=subject,
            content='This is a test email nothing more and nothing less',
        )
        [obj.contacts.add(parent) for parent in Parent.objects.all()]
        obj.save()

    def test_access_admin(self):
        resp = self.client.get('/admin/', follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_parents_on_admin(self):
        resp = self.client.get('/admin/emails', follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_admin_info_view(self):
        resp = self.client.get('/admin/emails/email', follow=True)
        self.assertContains(resp, f'{Email.objects.count()} emails')

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_admin_view_contains_send_email_function(self):
        self.create_parents()
        self.create_test_email()

        change_url = reverse('admin:emails_email_changelist')

        resp = self.client.get(change_url, follow=True)

        self.assertContains(resp, 'Delete selected emails')
        self.assertContains(resp, 'Send selected email')

        self.client.post(change_url, data={
            'action': 'send_emails',
            ACTION_CHECKBOX_NAME: [Email.objects.first().pk, ],
        }, follow=True)

        self.assertEqual(len(mail.outbox), Parent.objects.count())

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_admin_view_contains_send_email_only_one_allowed(self):
        self.create_parents()
        self.create_test_email()
        self.create_test_email(subject='Another test email')

        change_url = reverse('admin:emails_email_changelist')

        resp = self.client.get(change_url, follow=True)

        self.assertContains(resp, 'Delete selected emails')
        self.assertContains(resp, 'Send selected email')

        self.client.post(change_url, data={
            'action': 'send_emails',
            ACTION_CHECKBOX_NAME: [obj.pk for obj in Email.objects.all()],
        }, follow=True)

        self.assertEqual(len(mail.outbox), 0)
