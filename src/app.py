import requests
import time
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import re

url = "https://ycharts.com/companies/TSLA/revenues"

# Agregar headers para evitar el error 403
headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
}

# Petición para descargar el fichero de Internet
response = requests.get(url, headers=headers)
time.sleep(5)  # Pausar 5 segundos para evitar sobrecargar el servidor

# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    # Parsear el contenido HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Buscar la tabla
    table = soup.find("table", class_="table")

    # Asegurarse de que la tabla existe
    if table:

        data = pd.DataFrame(columns = ["fecha", "ingreso"])

        # Recorrer todas las filas de la tabla
        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')
            if len(columns) >= 2:
                fecha = columns[0].text.strip()
                ingreso = columns[1].text.replace("$", "").replace(",", "").strip()
               
                # Limpiar y convertir el ingreso
                if ingreso.endswith("B"):
                    ingreso = float(ingreso.replace("B", "")) * 1e9  # Convertir de billones a número
                else:
                    ingreso = float(ingreso)  # Convertir a float si ya es un número simple
        
                # Agregar la fila al DataFrame usando loc[]
                data.loc[len(data)] = [fecha, ingreso]# Limpiar y convertir el ingreso

        # Filtrar valores vacíos
        data = data[data["ingreso"] != ""]

        # Convertir la columna 'Fecha' a formato datetime
        data['fecha'] = pd.to_datetime(data['fecha'])

        # Filtrar los datos para obtener solo los trimestres desde junio de 2009
        data = data[data['fecha'] >= '2009-06-01']

        # Convertir las fechas a cadenas para evitar el error con el tipo 'Timestamp'
        data['fecha'] = data['fecha'].dt.strftime('%Y-%m-%d')

        # Convertir DataFrame a lista de tuplas
        tesla_tuples = list(data.itertuples(index=False, name=None))

        # Conectar a la base de datos y crear la tabla
        con = sqlite3.connect('tesla.bd')
        cursor = con.cursor()

        cursor.execute('''
        DROP TABLE IF EXISTS Revenue;
         ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Revenue (
                date TEXT,
                revenue REAL
            )
        ''')

        cursor.executemany("INSERT INTO Revenue VALUES (?, ?)", tesla_tuples)
        con.commit()

        # Mostrar los datos insertados
        for row in cursor.execute("SELECT * FROM Revenue"):
            print(row)

        con.close()

    else:
        print("No se encontró la tabla en la página web.")
else:
    print(f"Error al acceder a la página. Código de estado: {response.status_code}")
