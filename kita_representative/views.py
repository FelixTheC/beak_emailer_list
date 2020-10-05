from django.views.generic import CreateView

from kita_representative.forms import KitaRepresentativeForm
from kita_representative.models import KitaRepresentative


class AssignToEmailer(CreateView):
    template_name = 'form.html'
    model = KitaRepresentative
    form_class = KitaRepresentativeForm
    success_url = 'https://www.beak-mh.de/'
