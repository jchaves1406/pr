from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

ubicacion = "/home/ubuntu/Downloads/chromedriver" #Ruta del driver
driver = webdriver.Chrome(ubicacion)

home_link = "https://www.fincaraiz.com.co/"
search_kw = "casas chapinero".replace(" ","+")

driver.get(home_link+"/finca-raiz/venta?ubicacion=casas+chapinero")
page = BeautifulSoup(driver.page_source, "html.parser")
# page
bloques = page.find_all("div", attrs={"class": "MuiCardContent-root"})
print(bloques[0])
