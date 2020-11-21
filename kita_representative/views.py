import os

from django.views.generic import CreateView

from kita_representative.forms import KitaRepresentativeForm
from kita_representative.models import KitaRepresentative


class AssignToEmailer(CreateView):
    template_name = 'form.html'
    model = KitaRepresentative
    form_class = KitaRepresentativeForm
    success_url = 'https://www.beak-mh.de/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reCAPTCHA_site_key'] = os.environ.get('reCAPTCHA_site_key', 'foobar')
        context['form_title'] = 'Anmeldung BEAK-Vertreter'
        return context
