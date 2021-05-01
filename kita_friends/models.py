from django.db import models

from additonal_utils.models import BigPrimaryKeyModel
from kita.models import Kita


class KitaFriends(BigPrimaryKeyModel):

    first_name = models.CharField(max_length=255, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)

    email = models.EmailField(blank=False, null=False)
    kita = models.ForeignKey(Kita, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta(BigPrimaryKeyModel.Meta):
        app_label = 'kita_friends'
        get_latest_by = 'created_at'
        ordering = ['-kita', '-name', '-first_name']
        unique_together = [['name', 'first_name', 'email', 'kita']]
        verbose_name = 'Kita-Friend'
        verbose_name_plural = 'Kita-Friends'

    def __str__(self):
        return f'{self.first_name} {self.name} - {self.kita.name}'
