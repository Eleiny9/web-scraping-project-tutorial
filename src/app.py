import requests
import time
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup


# Función para conectar a la base de datos
def conectar_bd():
    conexion = sqlite3.connect('tesla.bd')
    return conexion

# Función para crear la tabla (asegurarse de que existe)
def crear_tabla(conexion):
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Revenue (
            date TEXT,
            revenue REAL
        )
    ''')
    conexion.commit()

# Función para insertar datos en la base de datos
def insertar_datos(conexion, datos):
    cursor = conexion.cursor()
    cursor.executemany('''
        INSERT INTO Revenue (date, revenue) VALUES (?, ?)
    ''', datos)
    conexion.commit()

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

    # Convertir DataFrame a lista de tuplas
    datos = list(data.itertuples(index=False, name=None))

    # Conectar a la base de datos y crear la tabla
    con = conectar_bd()
    crear_tabla(con)

    # Insertar datos en la base de datos
    insertar_datos(con, datos)

    # Cerrar la conexión
    con.close()

    # Opcional: Mostrar el DataFrame
    print(data)

else:
    print(f"Error al acceder a la página. Código de estado: {response.status_code}")
