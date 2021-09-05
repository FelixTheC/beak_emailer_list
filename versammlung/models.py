from typing import Tuple

from django.db import IntegrityError
from django.db import models
from django.template import Context, Template

from emailer.models import send_single_email


class BestaetigungsEmail(models.Model):
    email_subject = models.CharField(max_length=255)
    email_text = models.TextField(help_text="Email text wird als html versendet.")
    aktiviert = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = ("-created_at", "aktiviert")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.pk and BestaetigungsEmail.objects.filter(aktiviert=True).count() > 0:
            raise IntegrityError("There can only be one active BestaetigungsEmail.")
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.email_subject} - active: {self.aktiviert}'


class Versammlung(models.Model):
    title = models.CharField(max_length=255, help_text="bsp.: Versammlung 28.09.2021")
    wann = models.DateField()
    wo = models.CharField(max_length=255, help_text="Rathhaussaal")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Versammlungen"

    def __str__(self):
        return self.title


class Teilnehmer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    versammlung = models.ForeignKey(Versammlung, related_name="member", on_delete=models.CASCADE)
    anmeldung_bestaetigt = models.BooleanField(default=False, editable=False)

    class Meta:
        unique_together = ("name", "email")
        verbose_name_plural = "Teilnehmer"

    def parse_email_content(self) -> Tuple[str, str]:
        email_confirmation = BestaetigungsEmail.objects.latest()
        email_text = Template(email_confirmation.email_text).render(Context({"name": self.name,
                                                                             "title": self.versammlung}))
        return email_confirmation.email_subject, email_text

    def send_confirmation_email(self):
        email_subject, email_content = self.parse_email_content()
        send_single_email(subject=email_subject, message=email_content, recipient=(self.email,), fail_silently=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.anmeldung_bestaetigt:
            self.send_confirmation_email()
            self.anmeldung_bestaetigt = True
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.name} - {self.email}'
