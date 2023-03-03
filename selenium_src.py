from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from pyvirtualdisplay import Display

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
print(bloques[0])
