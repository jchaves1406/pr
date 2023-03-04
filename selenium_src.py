from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from pyvirtualdisplay import Display
import pandas as pd
import datetime

display = Display(visible=0, size=(1920, 1080))
display.start()
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--remote-debugging-port=9222')

ubicacion = "/home/runner/work/pr/pr/chromedriver" #Ruta del driver
driver = webdriver.Chrome(ubicacion, options=options)

home_link = "https://www.fincaraiz.com.co/"
search_kw = "casas chapinero".replace(" ","+")

driver.get(home_link+"/finca-raiz/venta?ubicacion=casas+chapinero")
page = BeautifulSoup(driver.page_source, "html.parser")
# page
bloques = page.find_all("div", attrs={"class": "MuiCardContent-root"})

casas = []

for i, bloque in enumerate(bloques):
    # bloque.get_attribute_list
    atributos = []
    etiquetas_span = bloque.find_all('span')
    for span in etiquetas_span:
        # print(span.text.strip())
        atributos.append(span.text.strip())
    casas.append(atributos)

driver.quit()
display.stop()

palabras_clave = {
    "Bogotá": 0,
    "$": 1,
    "ha": 2,
    "ba": 3,
    "m²": 4
}

casas_df = []

for casa in casas:
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
print(df)
