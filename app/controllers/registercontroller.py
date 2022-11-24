import json
from django.views import View
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..models import Company, CustomUser
#from django.contrib.auth.models import User
#from django.contrib.auth import crea
import json
import sys
from ..middleware import verify_token
# Create your views here.

class RegisterController(View):

    user = None

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        verify = verify_token(request = request)
        if verify['success'] == False:
            return JsonResponse(verify, status= 402)
        self.user = verify['user']
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):

        js = json.loads(request.body)

        try:
            username = js['username']
            company = js['company']
            role = js['role']
            email = js['email']
            password = js['password']
            confirm_password = js['confirm_password']
        except Exception  as e:
            datos={'success': False, 'message': 'Datos incompletos'}
            return JsonResponse(datos)
        
        
        if(username==""):
            datos={'success': False, 'message': 'El nombre es obligatorio'}
            return JsonResponse(datos)

        if(company==""):
            datos={'success': False, 'message': 'Debe seleccionar una organización'}
            return JsonResponse(datos)
        
        if(role==""):
            datos={'success': False, 'message': 'Debe seleccionar un rol'}
            return JsonResponse(datos)

        if(email==""):
            datos={'success': False, 'message': 'El correo electrónico es obligatorio'}
            return JsonResponse(datos)

        if(password != confirm_password):
            datos={'success': False, 'message': 'Las contraseñas no coiciden'}
            return JsonResponse(datos)
        
        if (  (role in ["Administrador", "Usuario"]) == False ):
            datos={'success': False, 'message': 'El rol no existe.'}
            return JsonResponse(datos)

        users = CustomUser.objects.filter(email= email)
        if len(users)>0:
            datos={'success': False, 'message': 'El correo electrónico ya esta en uso'}
            return JsonResponse(datos)

        companies = Company.objects.filter(id= company)
        if len(companies)<=0:
            datos={'success': False, 'message': 'No se encontro la organización'}
            return JsonResponse(datos)

        try:

            user = CustomUser.objects.create_user(
                first_name =  username,
                username = email,
                company = Company(id = company),
                role = role,
                email = email,
                password = password
            )
        
        except Exception  as e:
            datos={'success': False, 'message': e}
            return JsonResponse(datos)
        
        datos={'success': True, 'message': 'Success'}
        return JsonResponse(datos)





    
