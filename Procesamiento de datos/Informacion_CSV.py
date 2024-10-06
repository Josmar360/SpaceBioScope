import pandas as pd

# Cargar el archivo CSV
file_path = 'datos_integrados.csv'  # Reemplaza con la ruta de tu archivo
data = pd.read_csv(file_path)

# Contar valores únicos en cada columna
unique_counts = data.nunique()

# Mostrar el nombre de la columna y la cantidad de valores únicos
print("Cantidad de valores únicos en cada columna:")
for column, count in unique_counts.items():
    print(f"{column}: {count} valores únicos")
