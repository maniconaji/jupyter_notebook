# Manejo de  datos
import pandas as pd                          # Manipular DataFrames y DataArrays
import numpy as np                           # Manipular array y otros algoritmos matematicos
from glob import glob                        # Encontrar ruta (path) de cada archivo
from functools import reduce
from datetime import datetime

def lectura_csv(path):
    #Apertura de 
    variable = path.split("_")[1]
    df = pd.read_csv(path, sep=";", dtype=str)
    df = df.iloc[:,:-1]
    # Definición fecha
    df['Fecha'] = '20'+df['FECHA (YYMMDD)']+' '+df['HORA (HHMM)']+'00'
    df['Fecha'] = pd.to_datetime(df['Fecha'], format="%Y%m%d %H%M%S")
    df          = df.drop(['FECHA (YYMMDD)', 'HORA (HHMM)'], axis=1)
    if ("Unnamed: 2" in df.columns) == True:
        df = df.rename({"Unnamed: 2": variable}, axis=1)
    if ('Registros validados' in df.columns) == True:
        df = df.drop(['Registros no validados','Registros preliminares'], axis=1)
        df = df.rename({'Registros validados': variable}, axis=1)
    df[variable] = df[variable].str.replace(',','.').astype(np.float32)
    return df

def lectura_todoscsv(paths):
    data = reduce(lambda left,right: pd.merge(left,right,on='Fecha', how="outer"), [lectura_csv(path) for path in paths])
    return data.set_index("Fecha").sort_index()