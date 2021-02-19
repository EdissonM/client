from datetime import datetime
import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression
import time

class analitica():
    ventana = 10
    pronostico = 3
    file_name = "data_base.csv"

    def __init__(self) -> None:
        self.load_data()

    def load_data(self):

        if not os.path.isfile(self.file_name):
            self.df = pd.DataFrame(columns=["fecha", "sensor", "valor"])
        else:
            self.df = pd.read_csv (self.file_name)

    def update_data(self, msj):
        msj_vetor = msj.split(",")
        new_data = {"fecha": msj_vetor[0], "sensor": msj_vetor[1], "valor": float(msj_vetor[2])}
        self.df = self.df.append(new_data, ignore_index=True)
    
    def print_data(self):
        print(self.df)
    
    def analitica_descriptiva(self):
        self.operaciones("temperatura")
        self.operaciones("densidad")

    def operaciones(self, sensor):
        df_filtrado = self.df[self.df["sensor"] == sensor]
        df_filtrado = df_filtrado["valor"]
        df_filtrado = df_filtrado.tail(self.ventana)
        print(df_filtrado.max(skipna = True))
        print(df_filtrado.min(skipna = True))
        print(df_filtrado.mean(skipna = True))
        print(df_filtrado.median(skipna = True))
        print(df_filtrado.std(skipna = True))


    def analitica_predictiva(self):
        df_filtrado = self.df[self.df["sensor"] == "temperatura"]
        df_filtrado = df_filtrado.tail(self.ventana)
        df_filtrado['fecha'] = pd.to_datetime(df_filtrado.pop('fecha'), format='%d.%m.%Y %H:%M:%S')
        df_filtrado['segundos'] = [time.mktime(t.timetuple()) - 18000 for t in df_filtrado['fecha']]
        tiempo = df_filtrado['segundos'].std(skipna = True, ddof=0)
        if tiempo == 0.0:
            return

        tiempo = tiempo.astype(int)
        ultimo_tiempo = df_filtrado['segundos'].iloc[-1]
        ultimo_tiempo = ultimo_tiempo.astype(int)
        range(ultimo_tiempo + tiempo,(self.pronostico + 1) * tiempo + ultimo_tiempo, tiempo)
        nuevos_tiempos = np.array(range(ultimo_tiempo + tiempo,(self.pronostico + 1) * tiempo + ultimo_tiempo, tiempo))

        X = df_filtrado["segundos"].to_numpy().reshape(-1, 1)  
        Y = df_filtrado["valor"].to_numpy().reshape(-1, 1)  
        linear_regressor = LinearRegression()
        linear_regressor.fit(X, Y)
        Y_pred = linear_regressor.predict(nuevos_tiempos.reshape(-1, 1))
        for tiempo, prediccion in zip(nuevos_tiempos, Y_pred):
            time_format = datetime.utcfromtimestamp(tiempo)
            print(prediccion[0])
            date_time = time_format.strftime('%d.%m.%Y %H:%M:%S')
            print(date_time)

    def guardar(self):
        self.df.to_csv(self.file_name, encoding='utf-8')
