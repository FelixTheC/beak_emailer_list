from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from versammlung.models import BestaetigungsEmail
from versammlung.models import Teilnehmer
from versammlung.models import Versammlung


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
    list_display = ("title", "wann", "wo")


@admin.register(Teilnehmer)
class TeilnehmerAdmin(admin.ModelAdmin):
    list_display = ("name", "versammlung", "anmeldung_bestaetigt")
    list_select_related = ("versammlung",)
    list_filter = (VersammlungListFilter,)
