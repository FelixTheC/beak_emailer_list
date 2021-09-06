from django.contrib import admin
from django.contrib import messages
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _

from versammlung.models import BestaetigungsEmail
from versammlung.models import Location
from versammlung.models import NotEnoughSpace
from versammlung.models import Teilnehmer
from versammlung.models import Versammlung


TARGET = "_self"


class VersammlungListFilter(admin.SimpleListFilter):
    title = _('Versammlung')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'versammlung'

    def lookups(self, request, model_admin):
        return Versammlung.objects.all().values_list("pk", "title")

    def queryset(self, request, queryset):
        if val := self.value():
            return queryset.filter(versammlung_id=val)
        else:
            return queryset


@admin.register(BestaetigungsEmail)
class BestaetigungsEmailAdmin(admin.ModelAdmin):
    list_display = ("email_subject", "email_text_slice", "aktiviert", "created_at")

    @admin.display(description='Email content')
    def email_text_slice(self, obj):
        return obj.email_text[:15]


@admin.register(Versammlung)
class VersammlungAdmin(admin.ModelAdmin):
    list_display = ("title", "wann", "location", "freie_sitze", "maximale_sitze", "zeige_teilnehmer")
    list_select_related = ("wo",)

    @admin.display
    def freie_sitze(self, obj):
        free_seats = obj.wo.max_teilnehmer - obj.member.count()
        color = "06ba00" if free_seats > 5 else "fca428"
        return format_html(
            '<span style="color: #{};font-weight: bold;">{}</span>', color, free_seats
        )

    @admin.display
    def maximale_sitze(self, obj):
        return format_html(
            '<span style="font-weight: bold;">{}</span>', obj.wo.max_teilnehmer
        )

    def location(self, obj: Versammlung):
        url = reverse("admin:versammlung_location_change", kwargs={"object_id": 1})
        return format_html(f'<a href="{url}" target="{TARGET}">{obj.wo}</a>')

    def zeige_teilnehmer(self, obj: Versammlung):
        path = urlencode({'versammlung__id': obj.id})
        url = f'{reverse("admin:versammlung_teilnehmer_changelist")}?{path}'
        return format_html(f'<a href="{url}" target="{TARGET}">{obj.member.count()} Teilnehmer</a>')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "addresse", "max_teilnehmer")


@admin.register(Teilnehmer)
class TeilnehmerAdmin(admin.ModelAdmin):
    list_display = ("name", "versammlungs_ort", "anmeldung_bestaetigt")
    list_select_related = ("versammlung",)
    list_filter = (VersammlungListFilter,)

    def versammlungs_ort(self, obj: Teilnehmer):
        url = reverse("admin:versammlung_location_change", kwargs={"object_id": obj.versammlung_id})
        return format_html(f'<a href="{url}" target="{TARGET}">{obj.versammlung}</a>')

    def get_exclude(self, request, obj=None):
        if obj is None:  # we want to add a new object
            return ("corona_status", )
        else:
            return []

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "versammlung":
            event_ids = [event.pk for event in Versammlung.objects.select_related("wo").all()
                         if event.member.count() < event.wo.max_teilnehmer]
            kwargs["queryset"] = Versammlung.objects.filter(id__in=event_ids)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except NotEnoughSpace:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Es können keine Teilnehmer mehr zu diesem Event hinzugefügt werden.')
        if not change:
            messages.add_message(request, messages.INFO, 'Bestätigungs email wurde versendet')
