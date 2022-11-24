from email import message
import json
from django.views import View
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..models import  CustomUser, FinancialEntity, Phone, HistoryCall, HistoryCallDetail 
#from django.contrib.auth.models import User
import json
import numpy as np
from tablib import Dataset
from datetime import datetime, date, timedelta
import time
from ..middleware import verify_token
# Create your views here.

class HistoryCallController(View):

    user = None
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        
        verify = verify_token(request = request)
        if verify['success'] == False:
            return JsonResponse(verify, status= 402)
        self.user = verify['user']
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id = 0):

        init_date = request.GET.get('init_date')
        end_date = request.GET.get('end_date')

        if (id > 0):
            history_calls = list(  HistoryCall.objects.filter(id = id).values())
            if len(history_calls)>0:
                history_call = history_calls[0]
                datos={'success': True, 'message': 'Success', 'history_call': history_call}
            else:
                datos={'success': False, 'message': 'Proveedor no encontrado ..'}
            return JsonResponse(datos)
        else:
            users = list(CustomUser.objects.filter(company = self.user.company.id).values_list('id', flat=True))
            query = HistoryCall.objects.filter(user__in =  users).select_related('user').order_by('-id')
            if init_date  and end_date :
                new_end = date.fromisoformat(end_date) + timedelta(days = 1)
                query = query.filter(created_at__range=[date.fromisoformat(init_date), new_end ] )
                ##query = query.filter(created_at__gte = date.fromisoformat(init_date), created_at__lte = new_end )

            history_calls = list(query.values('user__username', 'id','name', 'created_at'))
            if len(history_calls)>0:
                datos={'success': True, 'message': 'Success', 'history_calls': history_calls}
            else:
                datos={'success': False, 'message': 'Historial de llamadas no encontrados ..'}
            return JsonResponse(datos)

    def validate_data_file(self, records):
        
        records_len = len(records[0])
        if records_len != 6:
            return { 'success': False, 'message': f'El archivo solo cuenta con { records_len } columnas de 6.'}
        count = 1
        for row in records:
            count += 1
            row = row[row != None]
            if len(row) != 6:
                return { 'success': False, 'message': f'La fila {count} esta incompleto.'}
            if row[0].isalpha() == False:
                return { 'success': False, 'message': f'La entidad financiera de la fila {count} debe ser solo texto.'}
            if str(row[1]).isnumeric() == False:
                return { 'success': False, 'message': f'El télefono de la fila {count} debe ser solo numeros.'}
            
            if len(str(row[1])) > 9:
                return { 'success': False, 'message': f'El télefono de la fila {count} debe tener menos de 9 digitos.'}

            try:
                time.strptime(str(row[4]), '%H:%M:%S')
                
            except ValueError:
                
                    return { 'success': False, 'message': f'La hora de duracion de la fila {count} no cumple con el formato.'}

            try:
                datetime.strptime(str(row[3]), '%Y-%m-%d %H:%M:%S')
                
            except ValueError:
                print(str(row[3]))
                return { 'success': False, 'message': f'La fecha de llamada de la fila {count} no cumple con el formato.'}

            try:
                time.strptime(str(row[5]), '%H:%M:%S')
                
            except ValueError:
                return { 'success': False, 'message': f'La hora de llamada de la fila {count} no cumple con el formato.'}
            
           
            if row[2].isalpha() == False:
                return { 'success': False, 'message': f'El estado de la fila {count} debe ser solo texto.'}
             
            if (  (row[2] in ["EFECTIVO", "RECHAZADO", "OCUPADO"]) == False ):
                return { 'success': False, 'message': f'El estado es incorrecto de la fila {count}.'}
            
        return { 'success': True, 'message': ''}

    def post(self, request):
        
        
        #Leemos el archivo excel 
        
        data_set = Dataset()        
        file = request.FILES.get(u'file')                
        data = data_set.load(file.read(), format='xlsx')    
        np_data = np.array(data)

        #validamos la data del archivo excel 

        validate = self.validate_data_file(np_data)
        if validate.get('success') == False:
            return JsonResponse(validate) 

        #validamos la data del archivo excel 
        list_financial_entity = np.unique(np_data[:,0])
        list_phone = np.vstack(set(map(tuple, np_data[:,[0, 1]]))) 
        
        #Obtenemos el usuario logeado y los usuarios del grupo de la organizacion que pertenece
        auth =  self.user 
        users = list(CustomUser.objects.filter(company = self.user.company.id).values_list('id', flat=True))

        #Buscamos el historial de llamdas si existe uno ya subido con ese nombre para renombrarlo
        history_call_found = list(HistoryCall.objects.filter(name_upload = file, user__in =  users).values())

        if len(history_call_found)==0:
            history_call = HistoryCall.objects.create(name= file,name_upload = file, user=auth)
        else:
            rn = file.name.split('.')
            rename =  f'{rn[0]} ({len(history_call_found)}).{rn[1]}'
            history_call = HistoryCall.objects.create(name= rename, name_upload= file, user=auth)
        
        #Buscamos la entidad financiera si no existe para crear uno nuevo
        for financial_entity in list_financial_entity:
            financial_entity = financial_entity.strip()
            financial_entities = list(FinancialEntity.objects.filter(name = financial_entity, user__in =  users).values())
            if len(financial_entities)==0:
                FinancialEntity.objects.create(name= financial_entity, user = auth)

        #Buscamos las entidades financieras por el nombre y grupo de usuarios de la organizacion
        financial_entities = FinancialEntity.objects.filter(name__in = list_financial_entity, user__in =  users).values()

        #Buscamos los telefonos financiera por la entidad financiera y grupo de usuarios de la organizacion
        phones = list(Phone.objects.filter(financial_entity__name__in= list_financial_entity, user__in =  users ).values())
        
        #creamos una lista para la creacion masiva de telefonos y verificamos si existe o no
        bulk_list_phone = list()
        for row in list_phone:
            financial_entity_name = row[0].strip()
            phone = row[1].strip()
            financial_entity = financial_entities.get(name = financial_entity_name)
            financial_entity = FinancialEntity(id = financial_entity['id'])
            found_phone = list(filter(lambda x:x["number"] == phone and x["financial_entity_id"] == financial_entity.id ,phones))
            if len(found_phone) == 0:
                bulk_list_phone.append(Phone( 
                        number= phone,
                        financial_entity= financial_entity,
                        user = auth
                    )
                )
        
        #creamos los telefonos nuevos masivamente si la lista tiene mas de uno 
        if len(bulk_list_phone)>0:
            Phone.objects.bulk_create(bulk_list_phone)

        #Buscamos los telefonos financiera por el numero
        phones = list(Phone.objects.filter(number__in = np.unique(np_data[:,1]) , user__in =  users ).values('id','number', 'financial_entity'))

        #Convertimos la coleccion de entidad financiera en una lista
        financial_entities = list(financial_entities)

        #creamos una lista para la creacion masiva del detalle de historial de llamadas
        bulk_list_history_call_detail  = list()
        for row in data:
            financial_entity_name = row[0].strip()
            phone = str(row[1]).strip()
            financial_entity = list(filter(lambda x:x["name"] == financial_entity_name ,financial_entities))[0]
            financial_entity = FinancialEntity(id = financial_entity['id'])
            phone = list(filter(lambda x:x["number"] == phone and x["financial_entity"] == financial_entity.id ,phones))[0]
            phone = Phone(id = phone['id'])
            call_date = row[3].strftime("%Y-%m-%d")  
  
            bulk_list_history_call_detail.append(HistoryCallDetail( 
                    history_call= history_call,
                    financial_entity= financial_entity,
                    phone= phone,
                    hour= row[5],
                    state= row[2],
                    call_duration = row[4],
                    call_date = call_date,
                )
            )

        #creamos el detalle del historial de llamadas masivamente si la lista tiene mas de uno 
        if len(bulk_list_history_call_detail)>0:
            HistoryCallDetail.objects.bulk_create(bulk_list_history_call_detail)
          
        datos={'success': True, 'message': 'Historial de llamadas guardado con éxito.'}
        return JsonResponse(datos)

