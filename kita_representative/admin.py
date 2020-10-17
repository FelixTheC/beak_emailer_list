from django.contrib import admin

from kita_representative.models import KitaRepresentative


class KitaRepresentativeAdminModel(admin.ModelAdmin):
    list_display = ('name', 'email', 'kita')
    list_filter = ('name', 'kita')


admin.site.register(KitaRepresentative, KitaRepresentativeAdminModel)

