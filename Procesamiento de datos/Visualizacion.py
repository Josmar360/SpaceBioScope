import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Simular un dataframe con datos morfológicos para ejemplo
datos = {
    'grupo': ['vuelo', 'vuelo', 'vuelo', 'control', 'control', 'control'],
    'tamaño_vasos': [0.45, 0.50, 0.55, 0.40, 0.43, 0.38]
}

df = pd.DataFrame(datos)

# Gráfico de cajas (boxplot) para comparar distribución del tamaño de vasos entre los grupos
plt.figure(figsize=(8, 6))
sns.boxplot(x='grupo', y='tamaño_vasos', data=df, palette='Set2')
plt.title('Comparación de tamaño de vasos entre ratones de vuelo y control')
plt.xlabel('Grupo')
plt.ylabel('Tamaño de vasos oculares')
plt.show()

# Gráfico de barras para comparar el tamaño promedio de vasos entre los grupos
plt.figure(figsize=(8, 6))
sns.barplot(x='grupo', y='tamaño_vasos', data=df, ci=None, palette='Set2')
plt.title('Tamaño promedio de vasos entre ratones de vuelo y control')
plt.xlabel('Grupo')
plt.ylabel('Tamaño promedio de vasos oculares')
plt.show()
