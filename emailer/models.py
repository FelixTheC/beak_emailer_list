from typing import List
from typing import Tuple

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import get_connection
from django.core.mail.message import EmailMessage
from django.db import models
from strongtyping.strong_typing import match_typing
from strongtyping.type_namedtuple import typed_namedtuple
from tinymce.models import HTMLField

from kita.models import Kita
from kita_representative.models import KitaRepresentative

MESSAGE_TYPE = List[Tuple[str, str, str, tuple]]

DefaultSignature = typed_namedtuple('DefaultSignature', ['text:str', ])
default_signature = DefaultSignature(text='')


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
            obj = EmailSignature.objects.filter(active=True).first()
        except ObjectDoesNotExist:
            return default_signature
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
    kitas = models.ManyToManyField(Kita,
                                   related_name='kitas',
                                   related_query_name='kita',
                                   null=True,
                                   blank=True)
    representatives = models.ManyToManyField(KitaRepresentative,
                                             related_name='parents',
                                             related_query_name='parent',
                                             null=True,
                                             blank=True)

    created_at = models.DateTimeField(blank=True,
                                      null=True,
                                      auto_now=True,
                                      db_index=True)

    sent = models.BooleanField(default=False,
                               blank=True,
                               null=True)

    greeting = models.ForeignKey(EmailSignature,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 default=EmailSignature.get_signature)

    def __str__(self):
        return f'Email from {self.created_at}'

    @match_typing
    def _send_emails(self, datatuple: MESSAGE_TYPE, fail_silently: bool) -> int:
        connection = get_connection(fail_silently=fail_silently)

        def create_html_email(subject: str, message: str, sender: str, recipient: tuple, conn):
            msg = EmailMessage(subject, message, sender, recipient, connection=conn)
            msg.content_subtype = 'html'
            return msg

        messages = [
            create_html_email(subject, message, sender, recipient, conn=connection)
            for subject, message, sender, recipient in datatuple
        ]

        return connection.send_messages(messages)

    def send_emails(self):
        subject = self.subject
        greeting = self.greeting if self.greeting is not None else default_signature
        message = f'{self.content}{greeting.text}'
        sender = 'info@beak-mh.de'
        recipient = [obj.email for obj in self.kitas.all()] + [obj.email for obj in self.representatives.all()]
        message_tuple = [(subject, message, sender, (recipient[i], )) for i in range(len(recipient))]
        # total_emails = send_mass_mail(message_tuple, fail_silently=False)
        total_emails = self._send_emails(message_tuple, fail_silently=False)
        self.sent = True
        self.save()
        return total_emails
