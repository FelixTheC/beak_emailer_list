import json
from concurrent.futures import ThreadPoolExecutor as PoolExecutor

from django.http import HttpRequest
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from strongtyping.strong_typing import match_typing

from kita.models import Kita


class KitaCRUDView(View):

    http_method_names = ['post', ]

    def dispatch(self, request, *args, **kwargs):
        if request.content_type == 'application/json':
            request.json_data = json.loads(request.body.decode(request.POST._encoding))
        else:
            request.json_data = None
        return super().dispatch(request, *args, **kwargs)

    @csrf_exempt
    @match_typing
    def post(self, request: HttpRequest, *args, **kwargs):
        if request.json_data is not None:
            data = request.json_data['data']
            with PoolExecutor(max_workers=4) as executor:
                threads = [executor.submit(self._save_kita_entry, data=d) for d in data]
                [t.result() for t in threads]
        return HttpResponse(status=200)

    @staticmethod
    @match_typing
    def _save_kita_entry(data: dict):
        street_key = 'street' if 'street' in data else 'street_name'
        postal_key = 'plz' if 'plz' in data else 'postal_code'

        num = int(data['number']) if data['number'] else 0
        postal = int(data[postal_key]) if data[postal_key] else 12345
        street = data[street_key] if data[street_key] else '-----'

        Kita(name=data['name'],
             email=data['email'],
             street_name=street,
             number=num,
             postal_code=postal).save()
