import os

from django.core.mail import send_mail
from django.db import models

from kita.models import Kita


class KitaRepresentative(models.Model):

    class Meta:
        app_label = 'kita_representative'
        get_latest_by = 'created_at'
        ordering = ['-kita', '-name', '-first_name']
        unique_together = [['name', 'first_name', 'email', 'kita']]

    first_name = models.CharField(max_length=255, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)

    email = models.EmailField(blank=False, null=False)
    kita = models.ForeignKey(Kita, on_delete=models.CASCADE)

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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update,
                     using=using, update_fields=update_fields)
        self.max_representatives()
