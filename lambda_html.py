from web_sc_functions import descargar_pagina
import json
import boto3
import datetime
import os
import subprocess

s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    try:
        # Instalar Xvfb si no se encuentra en el entorno
        if not os.path.exists('/opt/Xvfb'):
            subprocess.call(['sudo', 'yum', '-y', 'install', 'xorg-x11-server-Xvfb'])

        # Iniciar Xvfb
        xvfb_process = subprocess.Popen(['Xvfb', ':0', '-screen', '0', '1024x768x24'])

        # Realizar una tarea de captura de pantalla usando Xvfb
        subprocess.call(['import', '-display', ':0', '-window', 'root', '/tmp/screenshot.png'])

        # Detener Xvfb
        # xvfb_process.kill()
    except Exception as e:
        print(str(e))
        
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


# zappa deploy dev
# test: zappa invoke apps.f

# actualizar:
# zappa update dev
# borrar: zappa undeploy
