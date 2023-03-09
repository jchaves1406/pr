import json
import boto3
from selenium import webdriver
import datetime
from selenium.webdriver.chrome.service import Service
from pyvirtualdisplay import Display
import os


s3 = boto3.client('s3')

def lambda_handler(event, context):
    
        
    url = "https://www.fincaraiz.com.co/finca-raiz/venta?ubicacion=casas+chapinero"
    descargar_pagina(url)

    bucket_name = 'landing-casas-xxx'
    file_name = datetime.datetime.now().strftime('%Y-%m-%d') + '.html'
    s3.upload_file("/home/runner/work/pr/pr/"
                   + file_name, bucket_name, file_name)

    return {
        'statusCode': 200,
        'body': json.dumps(file_name + " guardado.")
    }

def descargar_pagina(url):
    display = Display(visible=0, size=(800, 600))
    display.extra_display_args = ['+extension', 'RANDR', '+render', '-noreset']
    xvfb_path = '/usr/bin/Xvfb'  # especifica la ruta de XVFB aquí
    os.environ['DISPLAY'] = ':99'  # indica el número del servidor X
    os.system(f'{xvfb_path} :99 -screen 0 1024x768x24 &')  # inicia el servidor X en segundo plano
    display.start()
    # Ruta del driver en el archivo yml
    ubicacion = "/home/ubuntu/Downloads/zappa/chromedriver"

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
    with open("/home/ubuntu/Downloads/zappa/"+archivo_html,
              "w", encoding='utf-8') as f:
        f.write(driver.page_source)

    driver.quit()
    display.stop()

# zappa deploy dev
# test: zappa invoke apps.f

# actualizar:
# zappa update dev
# borrar: zappa undeploy
