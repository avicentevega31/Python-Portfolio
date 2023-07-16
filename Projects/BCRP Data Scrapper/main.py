import requests
import pandas as pd
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")
import urllib.request
import re
from datetime import datetime
import ssl
import altair as alt
ssl._create_default_https_context = ssl._create_unverified_context
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from datetime import datetime
import calendar
import numpy as np

url = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01288PM-PN01289PM/xml/2013-1/2016-9/ing"

def convertir_fechas(fechas:list):
    diccionario_meses_esp_eng = {
    'Ene': 'Jan',
    'Feb': 'Feb',
    'Mar': 'Mar',
    'Abr': 'Apr',
    'May': 'May',
    'Jun': 'Jun',
    'Jul': 'Jul',
    'Ago': 'Aug',
    'Sep': 'Sep',
    'Oct': 'Oct',
    'Nov': 'Nov',
    'Dic': 'Dec'
    }
    fechas_eng = []
    for i in fechas:
        i = i.replace(str(i[:3]), diccionario_meses_esp_eng[str(i[:3])])
        ultimo_dia_mes = calendar.monthrange(datetime.now().year, datetime.strptime(i, '%b%y').month)[1]
        fecha_transformada = datetime.strptime(i, '%b%y').replace(day=ultimo_dia_mes)
        fechas_eng.append(fecha_transformada)
    return fechas_eng 

def scrapper_bcrpdata_naird(url: str):
    codigo = url.split('/')[6]
    uno = url.split('/')[8]
    dos = url.split('/')[9]
    url_archivo = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/'+codigo+'/xml/'+uno+'/'+dos+'/'

    # Realizar la solicitud GET a la URL y obtener el contenido XML
    response = requests.get(url_archivo)
    contenido_xml = response.content
    # Analizar el contenido XML
    root = ET.fromstring(contenido_xml)

    # Crear listas para almacenar los datos de fecha y valor
    fechas = []
    valores = []

    for period in root.iter('period'):
        fecha = period.attrib['name']
        fecha = ''.join(fecha.split('.'))
        fechas.append(fecha)
        valorx = []
        for i in period.findall('v'):
            valorx.append(float(i.text))
        valores.append(valorx)

    title = []
    titlex = []
    for i in root.iter('serie'):
        titlex.append(i.attrib['name'])
    title.append(titlex)

    df = pd.DataFrame(
        data = valores,
        columns= title[0],
        #index=fechas
        index=convertir_fechas(fechas)
    )
    return df

df = scrapper_bcrpdata_naird(url)
df.head(5)

plt.figure(figsize=(30, 10))
for col in range(df.shape[1]):
    y = df[df.columns[col]]
    x = y.index  # Convertir x a una lista

    plt.plot(
        x, 
        y,
        'b+-', 
        marker='o',
        linewidth=1.5, 
        markersize=5,
        label = df.columns[col]
        )
    

plt.legend()
# plt.xlabel('Eje X')
# plt.ylabel('Eje Y')
plt.title('Grafica 1.1: Índice de precios Lima Metroplitana (Índice 2009 = 100) - IPC')


plt.show()