import json
import boto3
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import datetime

def lambda_handler(event, context):
    # Ruta del driver en el archivo yml
    ubicacion = "/home/ubuntu/Downloads/zappa/chromedriver"

    servicio = Service(ubicacion)
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')

    # options.binary_location = os.getcwd() + "/bin/headless-chromium"
    driver = webdriver.Chrome(service=servicio, options=options)

    # especificar la ruta de XVFB en la variable de entorno DISPLAY
    os.environ['DISPLAY'] = ':99'

    url = "https://www.fincaraiz.com.co/finca-raiz/venta?ubicacion=casas+chapinero"
    driver.get(url)

    # escribir el contenido de la página en el archivo
    archivo_html = datetime.datetime.now().strftime('%Y-%m-%d') + '.html'
    with open("/home/ubuntu/Downloads/zappa/"+archivo_html,
              "w", encoding='utf-8') as f:
        f.write(driver.page_source)

    # haz scraping aquí
    

    driver.quit()
    return {
    'statusCode': 200,
    'body': json.dumps(" guardado.")
    }

# zappa deploy dev
# test: zappa invoke apps.f

# actualizar:
# zappa update dev
# borrar: zappa undeploy
