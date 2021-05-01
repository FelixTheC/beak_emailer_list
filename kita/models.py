from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from additonal_utils.models import BigPrimaryKeyModel


def validate_postal_code_number(val: int):
    if val < 10000 or val > 99999:
        raise ValidationError(f'{val} is not a valid Postalcode', params={'val': val})


class Kita(BigPrimaryKeyModel):
    name = models.CharField(max_length=255, blank=False, null=False)

    street_name = models.CharField(max_length=255, blank=False, null=False)
    number = models.CharField(max_length=20, blank=False, null=False)
    postal_code = models.PositiveIntegerField(blank=False, null=False,
                                              validators=(validate_postal_code_number, ))

    email = models.EmailField(blank=False, null=False)

    representative = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta(BigPrimaryKeyModel.Meta):
        app_label = 'kita'
        get_latest_by = 'created_at'
        ordering = ['name', ]
        indexes = [
            models.Index(fields=('name', 'email', 'created_at')),
        ]
        unique_together = [['name', 'street_name', 'number', 'postal_code', 'email', 'representative']]
        index_together = [
            ['name', 'email', 'representative'],
        ]

    def __str__(self):
        return self.name
