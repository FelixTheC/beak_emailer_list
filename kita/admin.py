from urllib.parse import urlencode

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from kita.models import Kita
from kita_representative.models import KitaRepresentative


@admin.register(Kita)
class KitaAdminModel(admin.ModelAdmin):
    list_display = ('name', 'street_name', 'email', 'created_at', 'view_kita_representatives')
    list_filter = ('name', )
    search_fields = ('name__startswith', )

    def view_kita_representatives(self, obj: Kita):
        count = KitaRepresentative.objects.filter(kita=obj).count()
        path = urlencode({'kita__id': obj.id})
        url = f'{reverse("admin:kita_representative_kitarepresentative_changelist")}?{path}'
        return format_html(f'<a href="{url}" target="_blank">{count} BEAK-Vertreter</a>')
