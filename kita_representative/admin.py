from django.contrib import admin
from django.contrib import messages
from django.db.models import QuerySet

from kita_representative.models import KitaRepresentative


def send_to_newsletter(modeladmin, request, queryset: QuerySet):
    results = []
    for obj in queryset:
        results.append(obj.send_copy_to_newsletter_plugin())
    messages.info(request, f'#{len(results)} profiles has been send. {results}')


send_to_newsletter.short_description = 'Send details to newsletter'


@admin.register(KitaRepresentative)
class KitaRepresentativeAdminModel(admin.ModelAdmin):
    list_display = ('created_at', 'name', 'email', 'kita')
    list_filter = ('name', 'kita')
    search_fields = ('kita__name__startswith',
                     'name__startswith',
                     'email__contains')
    actions = (send_to_newsletter, )
