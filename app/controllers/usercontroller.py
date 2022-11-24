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

class UserController(View):

    user = None

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        verify = verify_token(request = request)
        if verify['success'] == False:
            return JsonResponse(verify, status= 402)
        self.user = verify['user']
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        auth = self.user

        
        query = CustomUser.objects.select_related('company').order_by('-date_joined')
        if( auth.role == 'Administrador'):
            query = query.filter(company = auth.company)
        if( auth.role == 'Usuario'):
            query = query.filter(id = auth.id)

        users = list(query.values('username', 'email', 'company__name', 'date_joined'))
        if len(users)>0:
            datos={'success': True, 'message': 'Success', 'users': users}
        else:
            datos={'success': False, 'message': 'Usuarios no encontrados ..'}
        return JsonResponse(datos)
