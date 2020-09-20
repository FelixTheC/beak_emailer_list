from django.test import TestCase
from django.test import override_settings

from emailer.models import Email
from emailer.models import EmailSignature
from kita.models import Kita
from kita_representative.models import KitaRepresentative


class EmailModelTest(TestCase):

    def setUp(self) -> None:
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
        Kita.objects.all().delete()
        KitaRepresentative.objects.all().delete()
        Email.objects.all().delete()
        EmailSignature.objects.all().delete()

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_mass_mail(self):
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
        obj.send_emails()
