from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.core.mail import send_mass_mail
from tinymce.models import HTMLField

from kita.models import Kita
from kita_representative.models import KitaRepresentative


class EmailSignature(models.Model):

    class Meta:
        app_label = 'emailer'
        get_latest_by = 'created_at'

    text = HTMLField(blank=False, null=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank=True, null=True, auto_now=True, db_index=True)

    @classmethod
    def get_signature(cls):
        try:
            obj = EmailSignature.objects.first()
        except ObjectDoesNotExist:
            return None
        else:
            return obj

    def __str__(self):
        return self.text


class Email(models.Model):

    class Meta:
        app_label = 'emailer'
        get_latest_by = 'created_at'
        ordering = ['-created_at', ]

    subject = models.CharField(max_length=255, blank=False, null=False)
    # content = models.TextField(blank=False, null=False)
    content = HTMLField(blank=False, null=False)
    kitas = models.ManyToManyField(Kita, related_name='kitas', related_query_name='kita',
                                   null=True, blank=True)
    representatives = models.ManyToManyField(KitaRepresentative, related_name='parents', related_query_name='parent',
                                             null=True, blank=True)

    created_at = models.DateTimeField(blank=True, null=True, auto_now=True, db_index=True)

    sent = models.BooleanField(default=False, blank=True, null=True)

    greeting = models.ForeignKey(EmailSignature, on_delete=models.SET_NULL,
                                 null=True, blank=True, default=EmailSignature.get_signature)

    def __str__(self):
        return f'Email from {self.created_at}'

    def send_emails(self):
        subject = self.subject
        message = f'{self.content}{self.greeting.text if self.greeting is not None else ""}'
        sender = 'info@beak-mh.de'
        recipient = [obj.email for obj in self.kitas.all()] + [obj.email for obj in self.representatives.all()]
        message_tuple = [(subject, message, sender, (recipient[i], )) for i in range(len(recipient))]
        total_emails = send_mass_mail(message_tuple, fail_silently=False)
        self.sent = True
        self.save()
        return total_emails
