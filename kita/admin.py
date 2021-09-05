from urllib.parse import urlencode

from django.contrib import admin
from django.contrib import messages
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.html import format_html

from kita.models import Kita
from kita_representative.models import KitaRepresentative
import pandas as pd
from pathlib import Path


def kitas_to_csv(modeladmin, request, queryset: QuerySet):
    df = pd.DataFrame.from_records(Kita.objects.all().values())
    file_path = Path(__file__).parent / Path("kita.csv")
    df.to_csv(str(file_path.absolute()))
    messages.info(request, f'#{file_path}.')
    return

kitas_to_csv.short_description = 'Kitas to csv'


@admin.register(Kita)
class KitaAdminModel(admin.ModelAdmin):
    list_display = ('name', 'street_name', 'email', 'created_at', 'view_kita_representatives')
    list_filter = ('name',)
    search_fields = ('name__startswith', 'name__icontains',
                     'street_name__startswith', 'street_name__icontains',
                     'email__startswith', 'email__icontains')
    actions = (kitas_to_csv, )

    def view_kita_representatives(self, obj: Kita):
        count = KitaRepresentative.objects.filter(kita=obj).count()
        path = urlencode({'kita__id': obj.id})
        url = f'{reverse("admin:kita_representative_kitarepresentative_changelist")}?{path}'
        return format_html(f'<a href="{url}" target="_blank">{count} BEAK-Vertreter</a>')
