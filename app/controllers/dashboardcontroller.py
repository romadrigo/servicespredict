import json
from django.views import View
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..models import  Phone, Report, HistoryCallDetail, CategoryHour
from django.contrib.auth.models import User
import json
import numpy as np
from tablib import Dataset
from datetime import date
from datetime import datetime, timedelta
import pandas as pd
import xlwt
from django.db.models import Count
from ..middleware import verify_token
from ..prediction_range import getNameDay
# Create your views here.

class DashboardController(View):

    user = None

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        verify = verify_token(request = request)
        if verify['success'] == False:
            return JsonResponse(verify, status= 402)
        self.user = verify['user']
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):


        financial_entity = request.GET.get('financial_entity')
 
        query = Report.objects.select_related('phone').order_by('-predicted_at')

        if financial_entity:
            query = query.filter(phone__financial_entity__id=financial_entity,day__in = [1, 2, 3, 4, 5] )

        calendar =  list()
        pie =  list()
        bar =  list()
        reports = query.values('category_range', 'day','phone__number')        
        category_hour = list(CategoryHour.objects.filter().values('id', 'first', 'second','name'))
        WEEKDAYS = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5}

        for row in WEEKDAYS:
            number_day = WEEKDAYS[row]
            new_category_hour = list()
           
            for cat_hour in category_hour:
                clients = reports.filter(category_range = cat_hour['id'], day= number_day)        
                
                number_clients = []
                if len(clients):
                    np_data = pd.DataFrame(list(clients))
                    number_clients = list(np_data['phone__number'])
                

                new_category_hour.append({
                        "start": cat_hour['first'],
                        "end": cat_hour['second'],
                        "cant_clients" : len(list(clients)),
                        "clients": number_clients
                    }
                )
                
                find_pies = list(filter(lambda x:x["range"] == cat_hour['name']  ,pie))
                if len(find_pies) == 0:
                    pie.append({
                            "range": cat_hour['name'],
                            "cant_clients": len(list(reports.filter(category_range = cat_hour['id']))) 
                        }
                    )
                    
            calendar.append({
                    "day": row,
                    "hours": new_category_hour
                }
            )

            
            bar.append({
                    "day": getNameDay(number_day),
                    "cant_clients": len(list(reports.filter( day= number_day))) 
                }
            )
            

        if len(calendar) >0 and len(list(reports))>0:
            datos={'success': True, 'message': 'Success', 'calendar': calendar, 'bar': bar, 'pie': pie }
        else:
            datos={'success': False, 'message': 'Predicciones no encontrados ..'}
        return JsonResponse(datos)

