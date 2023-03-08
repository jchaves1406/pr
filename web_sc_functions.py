from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pyvirtualdisplay import Display
import pandas as pd
import datetime


def descargar_pagina(url):
    display = Display(visible=0, size=(1920, 1080))
    display.start()
    # Ruta del driver en el archivo yml
    ubicacion = "/home/runner/work/pr/pr/chromedriver"

    servicio = Service(ubicacion)
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')
    driver = webdriver.Chrome(service=servicio, options=options)

    driver.get(url)

    # escribir el contenido de la página en el archivo
    archivo_html = datetime.datetime.now().strftime('%Y-%m-%d') + '.html'
    with open("/home/runner/work/pr/pr/"+archivo_html,
              "w", encoding='utf-8') as f:
        f.write(driver.page_source)

    driver.quit()
    display.stop()


def leer_pagina(path):
    with open(path, 'r') as file:
        contenido_html = file.read()

    page = BeautifulSoup(contenido_html, "html.parser")
    return page


def obtener_bloques_informacion(page):
    bloques = page.find_all("div", attrs={"class": "MuiCardContent-root"})
    return bloques


def extraer_atributos_casa(bloques):
    casas = []
    for bloque in bloques:
        atributos = []
        etiquetas_span = bloque.find_all('span')
        for span in etiquetas_span:
            atributos.append(span.text.strip())
        casas.append(atributos)
    return casas


def crear_dataframe_casas(atributos_casas):
    palabras_clave = {
        "Bogotá": 0,
        "$": 1,
        "ha": 2,
        "ba": 3,
        "m²": 4
    }

    casas_df = []

    for casa in atributos_casas:
        # Crear un diccionario con los atributos de la casa
        casas_dict = {clave: "N/A" for clave in palabras_clave.keys()}
        for atributo in casa:
            for palabra_clave in palabras_clave:
                if palabra_clave in atributo:
                    casas_dict[palabra_clave] = atributo
                    break
        casas_df.append(casas_dict)

    df = pd.DataFrame(casas_df)

    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
    df.insert(0, 'FechaDescarga', fecha_actual)

    # Renombrar columnas
    nombres_columnas = {
        "FechaDescarga": "Fecha Descarga",
        "Bogotá": "Barrio",
        "$": "Valor",
        "ha": "NumHabitaciones",
        "ba": "NumBanos",
        "m²": "mts2"
    }

    df = df.rename(columns=nombres_columnas)
    return df


def generar_csv(df_casas):
    nombre_archivo = datetime.datetime.now().strftime('%Y-%m-%d') + '.csv'
    # Guardar dataframe en archivo CSV
    df_casas.to_csv(nombre_archivo, index=False)
