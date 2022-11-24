import json
from lib2to3.pgen2 import token
from django.views import View
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from ..models import  Company, CustomUser
import json
from django.db.models import Count
import time
#import jwt
from jose import jwt
from environs import Env
# Create your views here.

class ResetPasswordController(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, token = None):

        if token == None:
            datos = {'success': False, 'message': 'El token es obligatorio'} 
            return JsonResponse(datos)

        users = CustomUser.objects.filter(token_reset_password= token)
        if len(users)>0:
            datos = {'success': True, 'message': 'success'}
        else:
            datos = {'success': False, 'message': 'Token no encontrado'}

        return JsonResponse(datos)


    def post(self, request, token = None):

        if token == None:
            datos = {'success': False, 'message': 'El token es obligatorio'} 
            return JsonResponse(datos)

        js = json.loads(request.body)

        try:
            
            password = js['password']
            confirm_password = js['confirm_password']

        except Exception  as e:
            datos={'success': False, 'message': 'Datos incompletos'}
            return JsonResponse(datos)

        if len(str(password))<6:
            datos={'success': False, 'message': 'La contraseña debe tener al menos 6 digitos'}
            return JsonResponse(datos)

        if(password != confirm_password):
            datos={'success': False, 'message': 'Las contraseñas no coiciden'}
            return JsonResponse(datos)

        users = CustomUser.objects.filter(token_reset_password= token)
        if len(users)>0:
            user = CustomUser.objects.get(token_reset_password= token)
            user.token_reset_password = ""
            user.set_password(password)
            user.save()
            datos = {'success': True, 'message': 'success'}
        else:
            datos = {'success': False, 'message': 'Token no encontrado'}

        return JsonResponse(datos)





    
