import time
from bs4 import BeautifulSoup
import requests



# Seleccionar el recurso a descargar
url = "https://ycharts.com/companies/TSLA/revenues"

# Petición para descargar el fichero de Internet
fichero = requests.get(url, time.sleep(5)).text

if "403 ERROR" in fichero:
    headers = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    request = requests.get(url,headers=headers)
    time.sleep(5)
    fichero = request.text


soup = BeautifulSoup(fichero, "html.parser")

table = soup.find_all("table", class_="table")

print(table)


