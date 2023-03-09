import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def lambda_handler(event, context):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"

    # especificar la ruta de XVFB en la variable de entorno DISPLAY
    os.environ['DISPLAY'] = ':99'

    # Ruta del driver en el archivo yml
    ubicacion = "/home/runner/work/pr/pr/chromedriver"
    driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome(service=servicio, options=options)
    url = "https://www.fincaraiz.com.co/finca-raiz/venta?ubicacion=casas+chapinero"
    driver.get(url)

    # haz scraping aquí
    

    driver.quit()

# zappa deploy dev
# test: zappa invoke apps.f

# actualizar:
# zappa update dev
# borrar: zappa undeploy
