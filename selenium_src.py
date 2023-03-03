from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
d = webdriver.Chrome('/home/<user>/chromedriver',chrome_options=chrome_options)
d.get('https://www.google.nl/')

ubicacion = "/home/runner/work/pr/pr/chromedriver" #Ruta del driver
driver = webdriver.Chrome(ubicacion)

home_link = "https://www.fincaraiz.com.co/"
search_kw = "casas chapinero".replace(" ","+")

driver.get(home_link+"/finca-raiz/venta?ubicacion=casas+chapinero")
page = BeautifulSoup(driver.page_source, "html.parser")
# page
bloques = page.find_all("div", attrs={"class": "MuiCardContent-root"})
print(bloques[0])
