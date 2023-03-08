import json
import boto3
import xvfbwrapper
from selenium import webdriver
import datetime



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
    xvfb = xvfbwrapper.Xvfb()
    xvfb.start()

    ubicacion = "/home/ubuntu/Downloads/zappa/chromedriver"
    servicio = webdriver.chrome.service.Service(ubicacion)
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--headless') # agregar esta línea para que la navegación sea sin interfaz gráfica
    driver = webdriver.Chrome(service=servicio, options=options)

    driver.get(url)

    archivo_html = datetime.datetime.now().strftime('%Y-%m-%d') + '.html'
    with open("/home/ubuntu/Downloads/zappa/"+archivo_html, "w", encoding='utf-8') as f:
        f.write(driver.page_source)

    driver.quit()
    xvfb.stop()

# zappa deploy dev
# test: zappa invoke apps.f

# actualizar:
# zappa update dev
# borrar: zappa undeploy
