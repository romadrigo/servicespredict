import json
from django.views import View
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..models import  HistoryCallDetail 
import json
from ..middleware import verify_token
# Create your views here.

class HistoryCallDetailController(View):

    user = None

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        verify = verify_token(request = request)
        if verify['success'] == False:
            return JsonResponse(verify, status= 402)
        self.user = verify['user']
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, history_call_id = 0):

        if (history_call_id > 0):
            history_call_details = list(  HistoryCallDetail.objects.select_related('phone').filter(history_call = history_call_id).values('state', 'hour', 'call_date', 'call_duration','phone__number', 'phone__financial_entity__name'))
            if len(history_call_details)>0:
                datos={'success': True, 'message': 'Success', 'history_call_details': history_call_details}
            else:
                datos={'success': False, 'message': 'Detalle de historial de llamadas no encontrados ..'}
            return JsonResponse(datos)
        else:
            datos={'success': False, 'message': 'No se encontría el historial de llamadas'}
            return JsonResponse(datos)
