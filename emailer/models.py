from typing import List
from typing import Tuple

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import get_connection
from django.core.mail.message import EmailMessage
from django.db import models
from strongtyping.strong_typing import match_typing
from strongtyping.type_namedtuple import typed_namedtuple
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE

from kita.models import Kita
from kita_friends.models import KitaFriends
from kita_representative.models import KitaRepresentative
from scheduler.commander import schedule_me

MESSAGE_TYPE = List[Tuple[str, str, str, tuple]]

DefaultSignature = typed_namedtuple('DefaultSignature', ['text:str', ])
default_signature = DefaultSignature(text='')

EMAIL_SENDER = 'info@beak-mh.de'


def send_single_email(subject: str, message: str, recipient: tuple, fail_silently: bool):
    connection = get_connection(fail_silently=fail_silently)
    msg = EmailMessage(subject, message, EMAIL_SENDER, recipient, connection=connection)
    msg.content_subtype = 'html'

    return connection.send_messages([msg, ])


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
    friends = models.ManyToManyField(KitaFriends,
                                     related_name='friends',
                                     related_query_name='friends',
                                     null=True,
                                     blank=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now=True, db_index=True)

    sent = models.BooleanField(default=False,
                               blank=True,
                               null=True)

    greeting = models.ForeignKey(EmailSignature,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 default=EmailSignature.get_signature)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        recipients = [obj.email for obj in self.kitas.all()] + [obj.email for obj in self.representatives.all()]
        [EmailDraft.objects.create(email=self, recipient=rcp) for rcp in recipients]

    def __str__(self):
        return f'Email from {self.created_at}'

    def send_emails(self):
        send_emails_interval()
        self.sent = True
        self.save()
        return calc_amount_emails()


class EmailDraft(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    recipient = models.EmailField()
    sent = models.BooleanField(default=False, blank=True)

    def send_email(self):
        email_obj = self.email
        subject = email_obj.subject
        greeting = email_obj.greeting if email_obj.greeting is not None else default_signature
        message = f'{email_obj.content}{greeting.text}'
        send_single_email(subject=subject, message=message, recipient=(self.recipient, ), fail_silently=False)
        self.sent = True
        self.save()
        return 1

    def __str__(self):
        return f'{self.recipient} - sent: {self.sent}'


def calc_amount_emails():
    return EmailDraft.objects.filter(sent=False).count()


# send 20 emails per hour (3600 seconds = 1hour)
@schedule_me(total_runs=calc_amount_emails, wait_seconds=3600, max_per_round=25)
def send_emails_interval():
    """
    Send emails in an interval
    """
    next_email = EmailDraft.objects.filter(sent=False).first()
    if next_email:
        next_email.send_email()
        next_email.sent = True
        next_email.save()
        return "email send"
    return "no emails"
