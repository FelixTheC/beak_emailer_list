from django.contrib import admin
from django.contrib import messages
from django.db.models import QuerySet

from emailer.forms import EmailForm
from emailer.forms import EmailSignatureForm
from emailer.models import Email
from emailer.models import EmailSignature


def send_emails(modeladmin, request, queryset: QuerySet):
    if len(queryset) > 1:
        messages.add_message(request, messages.ERROR, 'Only one email at a time can be chosen.')
        return
    queryset[0].send_emails()


send_emails.short_description = 'Send selected email'


class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at', 'sent')
    actions = (send_emails, )
    form = EmailForm


class EmailSignatureAdmin(admin.ModelAdmin):
    list_display = ('active', 'created_at')
    form = EmailSignatureForm


admin.site.register(Email, EmailAdmin)
admin.site.register(EmailSignature, EmailSignatureAdmin)
