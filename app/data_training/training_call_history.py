import pandas as pd
import numpy as np
from tablib import Dataset
import csv

list_documents =  [5] #[ 2, 3, 4, 5]

def create_data_set(number):
    data_set = Dataset()
    name_file = f'app/data_training/history_call_{number}_handle_hours.csv'
    print(name_file)
    datos = pd.read_csv(name_file, sep=';', header=None)
    datos =  np.array(datos)
    filtered = filter(lambda data: data[2] == 'EFECTIVO',datos)
    datos = np.array(list(filtered))
    phones = np.unique(datos[:,1])
    f = open( f'app/data_sets/history_call_{number}_efectives_handle_hours.csv', 'w', encoding='UTF8', newline='')
    writer = csv.writer(f)
    for row in phones:
        print(row)    
        rows = np.array(list(filter(lambda data: data[1] == row ,datos)))
        result = ""
        list_hours = list()
        for item in rows:
            hour= item[5][0:5]         
            if result == "":
                result = hour
                list_hours.append(result)
                print(result)
            list_hours.append(hour)
        
        print(list_hours)
        writer.writerow(list_hours)
    f.close()

for row in list_documents:
    create_data_set(row)