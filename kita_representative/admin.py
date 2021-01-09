from django.contrib import admin

from kita_representative.models import KitaRepresentative


@admin.register(KitaRepresentative)
class KitaRepresentativeAdminModel(admin.ModelAdmin):
    list_display = ('name', 'email', 'kita')
    list_filter = ('name', 'kita')
    search_fields = ('kita__name__startswith',
                     'name__startswith',
                     'email__contains')
