import json
from django.views import View
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..models import  Phone, Report, HistoryCallDetail, CustomUser, CategoryHour
#from django.contrib.auth.models import User
import json
import numpy as np
from tablib import Dataset
#import datetime 
from datetime import  datetime ,timedelta
from ..prediction import Prediction
import pandas as pd
import xlwt
from django.http import HttpResponse
from ..middleware import verify_token
from ..prediction_range import predict_range_hours, getNumberDay, getNameDay
# Create your views here.

class PredictionController(View):

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

        bulk_list =  list()
        reports = query.values('category_range', 'day','phone__number')        
        category_hour = list(CategoryHour.objects.filter().values('id', 'first', 'second'))
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
            bulk_list.append({
                    "day": row,
                    "hours": new_category_hour
                }
            )

        if len(bulk_list) >0 and len(list(reports))>0:
            datos={'success': True, 'message': 'Success', 'predictions': bulk_list}
        else:
            datos={'success': False, 'message': 'Predicciones no encontrados ..'}
        return JsonResponse(datos)


    def post(self, request):
        auth = self.user #CustomUser.objects.get(id=9)
        js = json.loads(request.body)
        financial_entity = js['financial_entity']
        phone = js['phone']

        query = HistoryCallDetail.objects
        if financial_entity:
            query = query.filter(financial_entity=financial_entity )
        if phone:
            phones = Phone.objects.filter(number= phone.strip()).values_list('id', flat=True)
            #print(phones)
            if len(phones)>0:
                query = query.filter(phone__in= phones )
            else:
                datos={'success': False, 'message': 'Teléfono no encontrado..'}
                return JsonResponse(datos)
        
        reports = query.filter(state= 'EFECTIVO' ).values()
        
        if(len(reports)):
            bulk_list  = list()
            #print('range hours')
            #print(list(reports))
            datosRange_main = pd.DataFrame(list(reports))
            datosRange = datosRange_main
            datosDay = datosRange_main

            mlr = predict_range_hours()
            datosRange['hour'] = datosRange['hour'].apply(lambda x: int(x.replace(':','')))

            conditions = [
                (datosRange['hour'] <= 110000),
                (datosRange['hour'] > 110000) & (datosRange['hour'] <= 140000),
                (datosRange['hour'] > 140000) & (datosRange['hour'] <= 170000),
                (datosRange['hour'] > 170000)]
            choices = [1, 2, 3, 4]
            datosRange['range'] = np.select(conditions, choices)
            datosRange['count'] = datosRange.groupby(['phone_id','range'])['range'].transform('count')
            
            datosRange = datosRange.drop_duplicates(subset=['phone_id','range','count'])
            datosRange = datosRange.pivot(index='phone_id', columns='range', values='count').reset_index().fillna(0)
            datosRangeComplet = datosRange
            #print(datosRangeComplet)
            datosRange = datosRange.drop('phone_id', axis=1)
            datosRange['result'] = mlr.predict(datosRange)
            #print(datosRange)
            #print('###########################')
            ###########################
            

            
            datosDay['weekdays'] = datosDay["call_date"].apply(lambda x: getNumberDay(x))
            datosDay['count'] = datosDay.groupby(['phone_id','weekdays'])['weekdays'].transform('count')
            datosDay = datosDay.drop_duplicates(subset=['phone_id','weekdays','count'])
            datosDay = datosDay.pivot(index='phone_id', columns='weekdays', values='count').reset_index().fillna(0)
            datosDayComplet = datosDay
            print(datosDayComplet)
            datosDay = datosDay.drop('phone_id', axis=1)
            datosDay['result'] = 0

            count = 0
            while count <= len(datosDay)-2:
                itemMaxValue = max(datosDay.iloc[count].items(), key=lambda x : x[1])
                
                datosDay['result'][count] = itemMaxValue[0]
                count += 1
            #print(datosDay)

            for x in range(len(datosRangeComplet)):
                find_reports = []
                phone_id = datosRangeComplet['phone_id'][x]
                phone_id2 = datosDayComplet['phone_id'][x]
                category_range = round(datosRange['result'][x])
                day = datosDay['result'][x]

                #print('category_range #####')
                #print(datosRange['result'][x])
                #print(category_range)
                

                find_reports = Report.objects.filter(phone = phone_id).order_by('-predicted_at').values()

                if(len(find_reports)):
                    new_category_range = CategoryHour(id = category_range)
                    Report.objects.filter(id = phone_id).update(category_range = new_category_range, day = day, predicted_at= datetime.now(), user= auth )
                else:
                    new_phone = Phone(id = phone_id)
                    new_category_range = CategoryHour(id = category_range)
                    bulk_list.append( Report( 
                            phone= new_phone,
                            category_range= new_category_range,
                            day= day,
                            prediction_result= "",
                            predicted_at= datetime.now(),
                            user= auth 
                        )
                    )
            if len(bulk_list)>0:

                Report.objects.bulk_create(bulk_list)
       


        datos={'success': True, 'message': 'Success'}
        return JsonResponse(datos)
    

    

class PredictionExportController(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        # init_date = request.GET.get('init_date')
        # end_date = request.GET.get('end_date')
        financial_entity = request.GET.get('financial_entity')
        # phone = request.GET.get('phone')        
        query = Report.objects.select_related('phone').select_related('category_range').order_by('-predicted_at')
        # if init_date  and end_date :
        #     #query = query.filter(predicted_at__range=[date.fromisoformat(init_date), date.fromisoformat(end_date) ] )
        #     new_end = date.fromisoformat(end_date) + timedelta(days = 1)
        #     query = query.filter(predicted_at__gte = date.fromisoformat(init_date),predicted_at__lte = new_end )
        if financial_entity:
            query = query.filter(phone__financial_entity__id=financial_entity, day__in = [1, 2, 3, 4, 5])
        # if phone:
        #     phones = Phone.objects.filter(number= phone.strip()).values_list('id', flat=True)
        #     if len(phones)>0:
        #         query = query.filter(phone__in= phones )
        #     else:
        #         datos={'success': False, 'message': 'Teléfono no encontrado..'}
        #         return JsonResponse(datos)
        
        reports = list(query.values('day','category_range__name' , 'predicted_at', 'phone__number', 'phone__financial_entity__name'))


        response = HttpResponse(content_type='application/ms-excel')

        response['Content-Disposition'] = 'attachment; filename="reporte_prediccion.xls"'

        wb = xlwt.Workbook(encoding='utf-8')

        ws = wb.add_sheet("sheet1")

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Teléfono', 'Entidad financiera', 'Fecha de prediccion', 'Día disponible', 'Rango de hora disponible' ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        for my_row in reports:
            row_num = row_num + 1  
            predicted_at = my_row.get('predicted_at')
            if (predicted_at): predicted_at = my_row.get('predicted_at').strftime('%d/%m/%Y')
            ws.write(row_num, 0, my_row.get('phone__number'), font_style)
            ws.write(row_num, 1, my_row.get('phone__financial_entity__name'), font_style)
            ws.write(row_num, 2, str(predicted_at), font_style)
            ws.write(row_num, 3, str( getNameDay( int(my_row.get('day')) ) ), font_style)
            ws.write(row_num, 4, str(my_row.get('category_range__name')), font_style)

        wb.save(response)
        return response

    
