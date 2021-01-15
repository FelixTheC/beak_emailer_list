from smtplib import SMTPDataError
from urllib.parse import urlencode

from django.contrib import admin
from django.contrib import messages
from django.db.models import QuerySet
from django.template.defaultfilters import safe
from django.template.defaultfilters import striptags
from django.urls import reverse
from django.utils.html import format_html

from emailer.forms import EmailForm
from emailer.forms import EmailSignatureForm
from emailer.models import Email
from emailer.models import EmailSignature


def send_emails(modeladmin, request, queryset: QuerySet):
    if len(queryset) > 1:
        messages.add_message(request, messages.ERROR, 'Only one email at a time can be chosen.')
        return
    try:
        mails_send = queryset[0].send_emails()
    except SMTPDataError as err:
        messages.error(request, err)
    else:
        messages.info(request, f'#{mails_send} emails has been send.')


send_emails.short_description = 'Send selected email'


def switch_signature_state(modeladmin, request, queryset: QuerySet):
    [setattr(obj, 'active', not getattr(obj, 'active')) for obj in queryset]
    [obj.save() for obj in queryset]


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at', 'sent', 'signature_used')
    actions = (send_emails, )
    form = EmailForm

    def signature_used(self, obj: Email):
        if obj.greeting:
            url = reverse('admin:emailer_emailsignature_change',
                          kwargs={'object_id': obj.greeting.id})
            snippet = striptags(obj.greeting.text[:50]).strip()
            return format_html(f'<a href="{url}">{snippet} ...</a>')
        url = reverse('admin:emailer_emailsignature_add')
        path = urlencode({'from_email': obj.id, })
        uri = f'{url}?{path}'
        return format_html(f'<a href="{uri}" target="_blank"> + Add</a>')


@admin.register(EmailSignature)
class EmailSignatureAdmin(admin.ModelAdmin):
    list_display = ('active', 'created_at', 'snippet')
    list_display_links = ('active', 'created_at', 'snippet')
    actions = (switch_signature_state, )
    form = EmailSignatureForm

    def response_post_save_add(self, request, obj):
        from_email = int(request.GET.get('from_email'))
        email_obj = Email.objects.get(pk=from_email)
        email_obj.greeting = obj
        email_obj.save()
        return super().response_post_save_add(request, obj)

    def snippet(self, obj: EmailSignature):
        return striptags(obj.text[:50]).strip()
