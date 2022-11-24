import pandas as pd
import numpy as np
import datetime

from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

#

def getNumberDay(date):            
    WEEKDAYS = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7}
    now =  datetime.datetime.strptime(date, "%Y-%m-%d").date()
    day = WEEKDAYS[now.strftime("%A")]
    return day

def getNameDay(number_day):            
    WEEKDAYS = {1: 'Lunes',  2: 'Martes', 3: 'Miércoles', 4: 'Jueves', 5: 'Viernes', 6: 'Sábado', 7: 'Domingo'}
    day = WEEKDAYS[number_day]
    return day

def predict_range_hours():
    data = pd.read_csv("app/data_training/callHistory.csv", sep=';')
    datosRange = data[data["State"] == 'EFECTIVO'] 
    datosRange['Hour'] = datosRange['Hour'].apply(lambda x: int(x.replace(':','')))

    conditions = [
                (datosRange['Hour'] <= 110000),
                (datosRange['Hour'] > 110000) & (datosRange['Hour'] <= 140000),
                (datosRange['Hour'] > 140000) & (datosRange['Hour'] <= 170000),
                (datosRange['Hour'] > 170000)]
    choices = [1, 2, 3, 4]
    datosRange['Range'] = np.select(conditions, choices)
    datosRange['Count'] = datosRange.groupby(['Phone','Range'])['Range'].transform('count')
    datosRange = datosRange.drop_duplicates(subset=['Phone','Range','Count'])
    datosRange = datosRange.pivot(index='Phone', columns='Range', values='Count').reset_index().fillna(0)
    datosRange = datosRange.drop('Phone', axis=1)
    datosRange['Result'] = 0

    count = 0
    while count <= len(datosRange)-2:
        itemMaxValue = max(datosRange.iloc[count].items(), key=lambda x : x[1])
        datosRange['Result'][count] = itemMaxValue[0]
        count += 1

    X = datosRange.drop('Result', axis=1)
    y = datosRange['Result']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

    print(X_test)
    mlr = MLPRegressor(solver = 'lbfgs', max_iter=2000,activation='relu', alpha= 1e-5,hidden_layer_sizes=(300,), random_state=500)
    
    mlr.fit(X_train, y_train)

    print(mlr.score(X_train, y_train))
    return mlr
    #for x in result:
    #    print(str(round(x)))