import json
from django.views import View
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..models import  Company
from django.contrib.auth.models import User
import json
from ..middleware import verify_token
# Create your views here.

class CompanyController(View):

    user = None

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        verify = verify_token(request = request)
        if verify['success'] == False:
            return JsonResponse(verify, status= 402)
        self.user = verify['user']
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        companies = list(Company.objects.values())
        if len(companies)>0:
            datos={'success': True, 'message': 'Success', 'companies': companies}
        else:
            datos={'success': False, 'message': 'Organizaciones no encontrados ..'}
        return JsonResponse(datos)

    def post(self, request):

        js = json.loads(request.body)
        name = js['name']
        number = js['number']

        if name == None or name == "":
            return JsonResponse({'success': False, 'message': 'El nombre de organización es obligatorio'})
        if number == None or number == "":
            return JsonResponse({'success': False, 'message': 'El ruc de organización es obligatorio'})
        if len(number) != 20:
            return JsonResponse({'success': False, 'message': 'El ruc de organización debe tener 20 caracteres'})

        companies = list(Company.objects.filter(name = name).values())
        if len(companies)>0:
            return JsonResponse({'success': False, 'message': 'La organización ya fue creada anteriormente'})
        
        companies = list(Company.objects.filter(number= number).values())
        if len(companies)>0:
            return JsonResponse({'success': False, 'message': 'La organización ya fue creada anteriormente'})

        Company.objects.create(name= name, number= number)  
        datos={'success': True, 'message': 'Success'}
        return JsonResponse(datos)





    
