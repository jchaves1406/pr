from web_sc_functions import leer_pagina, obtener_bloques_informacion, extraer_atributos_casa, crear_dataframe_casas, generar_csv
import json
import boto3
import datetime

s3 = boto3.client('s3')


def save_csv():
    file_name_html = datetime.datetime.now().strftime('%Y-%m-%d') + '.html'

    bucket_html = 'landing-casas-xxx'
    s3.download_file(bucket_html, file_name_html, file_name_html)

    page = leer_pagina("/home/runner/work/pr/pr/"+file_name_html)
    bloques = obtener_bloques_informacion(page)
    atributos_casas = extraer_atributos_casa(bloques)
    df_casas = crear_dataframe_casas(atributos_casas)
    print(df_casas)
    generar_csv(df_casas)

    file_name_csv = datetime.datetime.now().strftime('%Y-%m-%d') + '.csv'
    bucket_name = 'casas-final-xxx'
    s3.upload_file(file_name_csv, bucket_name, file_name_csv)

    return {
        'statusCode': 200,
        'body': json.dumps(file_name_csv + " guardado.")
    }

save_csv()

# zappa deploy dev
# test: zappa invoke apps.f

# actualizar:
# zappa update dev
# borrar: zappa undeploy
