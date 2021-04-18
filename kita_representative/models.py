import os
from datetime import datetime

import requests
from django.core.mail import send_mail
from django.db import models

from kita.models import Kita


class KitaRepresentative(models.Model):

    class Meta:
        app_label = 'kita_representative'
        get_latest_by = 'created_at'
        ordering = ['-kita', '-name', '-first_name']
        unique_together = [['name', 'first_name', 'email', 'kita']]
        verbose_name = 'Kita-Representative'
        verbose_name_plural = 'Kita-Representatives'

    first_name = models.CharField(max_length=255, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)

    email = models.EmailField(blank=False, null=False)
    kita = models.ForeignKey(Kita, on_delete=models.CASCADE)
    created_at = models.DateField(default=datetime.now, auto_created=True)

    def __str__(self):
        return f'{self.first_name} {self.name} - {self.kita.name}'

    def max_representatives(self):
        existing_representatives = KitaRepresentative.objects.filter(kita__name=self.kita.name).count()
        if existing_representatives > int(os.environ.get('MAX_REPRESENTATIVES', 2)):
            send_mail(subject='Problem bei der BEAK-Verteilerliste',
                      message=f'Zu viele Elternvertreter fuer {self.kita.name} dringend die '
                              f'Kita kontaktieren email: {self.kita.email}',
                      from_email='info@beak-mh.de',
                      recipient_list=['vorstand@beak-mh.de', ],
                      fail_silently=True)

    def send_copy_to_newsletter_plugin(self):
        client_key = "4cad1229a6970a0547b803d7b10f38d34c859bed"
        client_secret = "4bde16dc6789bdc2e9c5d200c97a1f9ec065de1a"
        uri = f"https://www.beak-mh.de/wp-json/newsletter/v1/subscribe/"
        get_param = f"?client_key={client_key}&client_secret={client_secret}"
        url = f"{uri}{get_param}"
        data = {
            "email": self.email,
            "api_key": "2add286a-d13c-4385-b539-f91eeeb74ecb",
            "surname": self.first_name,
            "name": self.name,
            "lists": [1, 2],
            "profile_2": f"{self.kita.street_name} {self.kita.number}, {self.kita.postal_code} Berlin",
            "profile_3": self.kita.name,
            "profile_4": self.kita.email,
            "send_emails": "false"
        }
        if not self.kita:
            del data["profile_2"]
            del data["profile_3"]
            del data["profile_4"]
        resp = requests.post(url=url,
                             data=data,
                             # auth=(client_key, client_secret)
                             )
        return resp.status_code

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update,
                     using=using, update_fields=update_fields)
        self.max_representatives()
        self.send_copy_to_newsletter_plugin()
