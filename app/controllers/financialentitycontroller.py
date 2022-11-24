import json
from django.views import View
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..models import  FinancialEntity, CustomUser
import json
from ..middleware import verify_token
# Create your views here.

class FinancialEntityController(View):

    user = None

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        verify = verify_token(request = request)
        if verify['success'] == False:
            return JsonResponse(verify, status= 402)
        self.user = verify['user']
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id = 0):
        if (id > 0):
            financial_entities = list(FinancialEntity.objects.filter(id = id).values())
            if len(financial_entities)>0:
                financial_entity = financial_entities[0]
                datos={'success': True, 'message': 'Success', 'financial_entity': financial_entity}
            else:
                datos={'success': False, 'message': 'Entidad financiera no encontrado ..'}
            return JsonResponse(datos)
        else:
            users = list(CustomUser.objects.filter(company = self.user.company.id).values_list('id', flat=True))
            financial_entities = list(FinancialEntity.objects.filter(user__in =  users).values())
            if len(financial_entities)>0:
                datos={'success': True, 'message': 'Success', 'financial_entities': financial_entities}
            else:
                datos={'success': False, 'message': 'Entidad financieras no encontrados ..'}
            return JsonResponse(datos)


    def post(self, request):
        js = json.loads(request.body)
        FinancialEntity.objects.create(name=js['name'], user= 1)        
        datos={'success': True, 'message': 'Success'}
        return JsonResponse(datos)

    def put(self, request, id= 0):
        js = json.loads(request.body)
        financial_entities = list(FinancialEntity.objects.filter(id = id).values())
        if len(financial_entities)>0:
            financial_entity = FinancialEntity.objects.get(id = id)
            financial_entity.name = js['name']
            financial_entity.save()
            datos={'success': True, 'message': 'Success'}
        else:
            datos={'success': False, 'message': 'Entidad financiera no encontrado ..'}
        return JsonResponse(datos)  
    def delete(self, request, id= 0):

        financial_entities = list(FinancialEntity.objects.filter(id = id).values())
        if len(financial_entities)>0:
            FinancialEntity.objects.filter(id = id).delete()
            datos={'success': True, 'message': 'Success'}
        else:
            datos={'success': False, 'message': 'Entidad financiera no encontrado ..'}
        return JsonResponse(datos)

