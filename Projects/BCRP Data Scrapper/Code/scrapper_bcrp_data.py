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


class Scrapper_BCRP_Data:
    def __init__(self, url: str) -> None:
        self.url = url

    def scrapper_bcrpdata_naird(self):
        codigo = self.url.split('/')[6]
        uno = self.url.split('/')[8]
        dos = self.url.split('/')[9]
        url_archivo = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/'+codigo+'/xml/'+uno+'/'+dos+'/'

        # Realizar la solicitud GET a la self.url y obtener el contenido XML
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
            index=fechas
            #index=convertir_fechas(fechas)
        )
        return df