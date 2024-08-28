import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

# Url
url = "https://ycharts.com/companies/TSLA/revenues"

# Agregar headers para evitar el error 403
headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}

# Petición para descargar el fichero de Internet
response = requests.get(url, headers=headers)
time.sleep(5)  # Pausar 5 segundos

# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    # Parsear el contenido HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Buscar la tabla 
    table = soup.find("table", class_="table")

    fechas = []
    ingresos = []

    # Recorrer todas las filas de la tabla (excluyendo la primera, que suele ser el encabezado)
    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        if len(columns) >= 2:
            fecha = columns[0].text.strip()
            ingreso = columns[1].text.strip()
            fechas.append(fecha)
            ingresos.append(ingreso)

    # Crear DataFrame 
    data = pd.DataFrame({'Fecha': fechas, 'Ingresos': ingresos})

    # Convertir la columna de fechas a tipo datetime
    data['Fecha'] = pd.to_datetime(data['Fecha'])

    # Filtrar los datos para obtener solo los trimestres desde junio de 2009
    data = data[data['Fecha'] >= '2009-06-01']

    # Mostrar los datos
    print(data)

else:
    print(f"Error al acceder a la página. Código de estado: {response.status_code}")
