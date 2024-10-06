import pandas as pd
from pymongo import MongoClient

# Configura la conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Cambia la URL según tu configuración
db = client['SpaceBioScope']  # Cambia el nombre de la base de datos
collection = db['OSD-665']  # Cambia el nombre de la colección

# Lee los datos desde el archivo CSV
df = pd.read_csv('datos_integrados.csv')  # Cambia esto por la ruta a tu archivo

# Limpia y preprocesa el DataFrame (si es necesario)
# Aquí puedes agregar el código de limpieza que mencionamos anteriormente

# Convierte el DataFrame a un diccionario
data_dict = df.to_dict("records")

# Inserta los datos en MongoDB
collection.insert_many(data_dict)

# Verifica la inserción
print(f'Documentos insertados: {len(data_dict)}')
