import pandas as pd

# Cargar los datos desde archivos CSV con codificación UTF-8
# Cambia 'muestras.csv' por el nombre de tu archivo
muestras_df = pd.read_csv('Datos/OSD-665/OSD-665-assays.csv', encoding='utf-8-sig')
# Cambia 'ensayos.csv' por el nombre de tu archivo
ensayos_df = pd.read_csv('Datos/OSD-665/OSD-665-samples.csv', encoding='utf-8-sig')

# Visualiza los primeros registros de cada DataFrame para confirmar que se cargaron correctamente
print("Datos de Muestras:")
print(muestras_df.head())

print("\nDatos de Ensayos:")
print(ensayos_df.head())

# Realizar la fusión de los DataFrames en base a 'Nombre de muestra'
integrated_df = pd.merge(muestras_df, ensayos_df,
                         on='Nombre de muestra', how='inner')

# Visualiza los datos integrados
print("\nDatos Integrados:")
print(integrated_df.head())

# Guardar el DataFrame integrado en un nuevo archivo CSV con codificación UTF-8
integrated_df.to_csv('datos_integrados.csv', index=False, encoding='utf-8-sig')
print("\nDatos integrados guardados en 'datos_integrados.csv'.")
