import time
from bs4 import BeautifulSoup
import requests



# Seleccionar el recurso a descargar
url = "https://www.w3schools.com/python/ref_string_split.asp#:~:text=The%20split()%20method%20splits,default%20separator%20is%20any%20whitespace."

# Petición para descargar el fichero de Internet
fichero = requests.get(url, time.sleep(10))
print(fichero)

if fichero:
    soup = BeautifulSoup( fichero.text , 'html')
    print(soup)

"""td = soup.find_all("td", class_="text-right")

print(td)"""


