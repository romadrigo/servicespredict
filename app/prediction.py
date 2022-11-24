import pandas as pd
import numpy as np
import datetime

from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class Prediction():

    def formatHours(hours):        
        listhour = []
        for x in hours:
            x = x[0:5].replace(':','')
            listhour.append(int(x))
        return [listhour]

    def getFileNameTraining(number_file):
        return f'app/data_sets/history_call_{number_file}_efectives_handle_hours.csv'

    def formatResult(result):
        for x in result:
            x = str(round(x))
            b = int(x[-2:])
            if len(x) == 3:
                a = int(x[:1])
            else:
                a = int(x[:2])

            if b > 90:
                b = 00
                a = a + 1
            elif b > 59:
                b = b - 60
                a = a + 1

        return str(a).zfill(2) + ':'+ str(b).rjust(2,'0')+ ':'+ str(b).rjust(2,'0')

    def readData(nameFile):
        datos = pd.read_csv(nameFile, sep=',', header=None)

        y = datos.iloc[:, 0].apply(lambda x: x.replace(':',''))
        x = datos.drop(columns=datos.columns[0], axis=1)

        for column in x:
            x[column] = x[column].apply(lambda x: x.replace(':',''))

        X = x[:np.newaxis]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)

        print(X_test)
        mlr = MLPRegressor(solver = 'lbfgs', max_iter=1000,activation='relu', alpha= 1e-5,hidden_layer_sizes=(300,), random_state=500)

        mlr.fit(X_train, y_train)

        print(mlr.score(X_train, y_train))

        return mlr
