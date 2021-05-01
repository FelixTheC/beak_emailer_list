import os
from datetime import datetime

import requests
from django.conf import settings
from django.core.mail import send_mail
from django.db import models

from additonal_utils.models import BigPrimaryKeyModel
from kita.models import Kita


class KitaRepresentative(BigPrimaryKeyModel):

    first_name = models.CharField(max_length=255, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)

    email = models.EmailField(blank=False, null=False)
    kita = models.ForeignKey(Kita, on_delete=models.CASCADE)
    created_at = models.DateField(default=datetime.now, auto_created=True)

    class Meta(BigPrimaryKeyModel.Meta):
        app_label = 'kita_representative'
        get_latest_by = 'created_at'
        ordering = ['-kita', '-name', '-first_name']
        unique_together = [['name', 'first_name', 'email', 'kita']]
        verbose_name = 'Kita-Representative'
        verbose_name_plural = 'Kita-Representatives'

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
        client_key = settings.WP_NEWSLETTER_PLUGIN_KEY
        client_secret = settings.WP_NEWSLETTER_PLUGIN_SECRET
        uri = settings.WP_NEWSLETTER_PLUGIN_URI
        get_param = f"?client_key={client_key}&client_secret={client_secret}"
        url = f"{uri}{get_param}"
        data = {
            "email": self.email,
            "api_key": settings.WP_NEWSLETTER_PLUGIN_API_KEY,
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
