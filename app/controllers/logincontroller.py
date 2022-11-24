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

class LoginController(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):

        datos = datos={'success': False, 'message': 'Credenciales incorrectos'} 
        env = Env()
        env.read_env()
        secret_key = env("JWT_SECRET_KEY")
        js = json.loads(request.body)
        
        email = js['email']
        password = js['password']

        if(email == "" or password ==""):
            return JsonResponse(datos)

        try:
            user = CustomUser.objects.get(email= email)
            if user:
                if user.check_password(password):
                    token = jwt.encode({
                        "id": user.id,
                        "name": user.first_name,
                        "email": user.email,
                        "company_name": user.company.name,
                        "company_number": user.company.number,
                        "role": user.role,
                    }, secret_key, algorithm="HS256")

                    datos={'success': True, 'token': token}
        except Exception  as e:   

            return JsonResponse(datos)

        return JsonResponse(datos)





    
