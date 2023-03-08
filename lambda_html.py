from web_sc_functions import descargar_pagina
import json
import boto3
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


# zappa deploy dev
# test: zappa invoke apps.f

# actualizar:
# zappa update dev
# borrar: zappa undeploy
