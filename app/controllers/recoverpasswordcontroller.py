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
from django.core.mail import send_mail
import socket
import string    
import random

# Create your views here.

class RecoverPasswordController(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):

        #socket.getaddrinfo('localhost', 80)
        if bool(request.body) == False:
            datos = {'success': False, 'message': 'El correo electrónico debe ser obligatorio.'} 
            return JsonResponse(datos)

        js = json.loads(request.body)
        
        if bool(js) == False:
            datos = {'success': False, 'message': 'El correo electrónico debe ser obligatorio.'} 
            return JsonResponse(datos)

        email = js['email']

        if(email == ""):
            datos = {'success': False, 'message': 'El correo electrónico debe ser obligatorio.'} 
            return JsonResponse(datos)

        users = CustomUser.objects.filter(email= email).values('email','id')
        if len(users)>0:          
            user = users[0]      
            env = Env()
            env.read_env()
            url = env("URL")
            S = 10    
            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))                
            token = str(user['id'])+str(ran)+str(user['id']) 
            CustomUser.objects.filter(id = user['id']).update(token_reset_password= token)

            path_reset_password = url+'restart_password/'+token
            send_mail(
                'Restablecer contraseña del sistema de predicción',
                'Restablecer contraseña del sistema de predicción',                
                'rodriigogj@gmail.com',
                [user['email']],
                fail_silently=False,
                html_message = f'<h1>Sistema de predicción SSAWDM</h1><p>Recupera tu contraseña: <a target="_blank" href="{path_reset_password}">aqui</a></p>',
            )
            
            datos={'success': True, 'message': 'Revisar su correo electrónico por favor'}
        else:
            datos = {'success': False, 'message': 'El correo electrónico no esta registrado.'}    
        

        return JsonResponse(datos)





    
