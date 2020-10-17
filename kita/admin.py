from django.contrib import admin

from kita.models import Kita


class KitaAdminModel(admin.ModelAdmin):
    list_display = ('name', 'street_name', 'email', 'created_at')
    list_filter = ('name', )


admin.site.register(Kita, KitaAdminModel)
