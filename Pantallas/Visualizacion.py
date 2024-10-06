import pandas as pd
import pygame
import numpy as np
from pymongo import MongoClient
import seaborn as sns
import matplotlib.pyplot as plt

# Inicializa Pygame
pygame.init()
info_pantalla = pygame.display.Info()
ANCHO, ALTO = info_pantalla.current_w, info_pantalla.current_h
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Visualización de datos")

# Crea una lista de figuras para las gráficas
figuras = []


# Función para mostrar la gráfica actual


def mostrar_grafica(indice):
    # Cierra la figura antes de guardar
    plt.close(figuras[indice])

    # Guarda la figura en un archivo temporal
    figuras[indice].savefig('temp.png', dpi=300, bbox_inches='tight')

    # Carga la imagen en Pygame
    imagen = pygame.image.load('temp.png')
    # Redimensiona la imagen
    imagen = pygame.transform.scale(imagen, (ANCHO, ALTO))

    # Muestra la imagen en la pantalla
    screen.blit(imagen, (0, 0))
    pygame.display.flip()

# Función para crear las gráficas


def crear_graficas(db_id):
    # Configura la conexión a MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['SpaceBioScope']  # Cambia por el nombre de tu base de datos
    # Conectar a la colección usando el nombre definido
    collection = db[db_id]

    # Extrae los datos de la colección y los convierte en un DataFrame
    data = pd.DataFrame(list(collection.find()))

    # Verifica si el DataFrame está vacío
    if data.empty:
        print(f"No se encontraron datos en la colección: {db_id}")
        return  # Sale de la función si no hay datos

    # Asegúrate de que las columnas relevantes están presentes en el DataFrame
    print(data.columns)

    # Suponiendo que 'Valor del parámetro: hábitat' se refiere al grupo
    grupo_columna = 'Valor del parámetro: hábitat'

    # 1. Comparar la profundidad de lectura entre grupos
    fig1, ax1 = plt.subplots(figsize=(ANCHO / 100, ALTO / 100))
    sns.boxplot(data=data, x=grupo_columna,
                y='Valor del parámetro: Profundidad de lectura', palette='Set2', ax=ax1)
    plt.title('Comparación de la Profundidad de Lectura entre Grupos')
    plt.tight_layout()
    figuras.append(fig1)

    # 2. Contaminación por ARNr por grupo
    fig2, ax2 = plt.subplots(figsize=(ANCHO / 100, ALTO / 100))
    sns.boxplot(data=data, x=grupo_columna,
                y='Valor del parámetro: Contaminación por ARNr', palette='Set2', ax=ax2)
    plt.title('Contaminación por ARNr por Grupo')
    plt.tight_layout()
    figuras.append(fig2)

    # 3. Comparar el peso corporal en el momento de la eutanasia
    fig3, ax3 = plt.subplots(figsize=(ANCHO / 100, ALTO / 100))
    sns.boxplot(data=data, x=grupo_columna,
                y='Valor del parámetro: Peso corporal en el momento de la eutanasia', palette='Set2', ax=ax3)
    plt.title('Peso Corporal en el Momento de la Eutanasia por Grupo')
    plt.tight_layout()
    figuras.append(fig3)

    # 4. Comparar la edad en el momento de la eutanasia
    fig4, ax4 = plt.subplots(figsize=(ANCHO / 100, ALTO / 100))
    sns.boxplot(data=data, x=grupo_columna,
                y='Valor del parámetro: Edad en el momento de la eutanasia', palette='Set2', ax=ax4)
    plt.title('Edad en el Momento de la Eutanasia por Grupo')
    plt.tight_layout()
    figuras.append(fig4)

    # 5. Distribución del Tamaño del Fragmento por Grupo
    fig5, ax5 = plt.subplots(figsize=(ANCHO / 100, ALTO / 100))
    sns.histplot(data=data, x='Valor del parámetro: Tamaño del fragmento',
                 hue=grupo_columna, multiple="stack", kde=True, ax=ax5)
    plt.title('Distribución del Tamaño del Fragmento por Grupo')
    plt.tight_layout()
    figuras.append(fig5)

    # 6. Gráfico de dispersión para comparar Contaminación por ARNr y Profundidad de Lectura
    fig6, ax6 = plt.subplots(figsize=(ANCHO / 100, ALTO / 100))
    sns.scatterplot(data=data, x='Valor del parámetro: Profundidad de lectura',
                    y='Valor del parámetro: Contaminación por ARNr', hue=grupo_columna, palette='Set2', alpha=0.7, ax=ax6)
    plt.title('Contaminación por ARNr vs Profundidad de Lectura')
    plt.tight_layout()
    figuras.append(fig6)

    # 7. Comparar el peso corporal y la edad en el momento de la eutanasia
    fig7, ax7 = plt.subplots(figsize=(ANCHO / 100, ALTO / 100))
    sns.violinplot(data=data, x=grupo_columna, y='Valor del parámetro: Peso corporal en el momento de la eutanasia',
                   inner='quartile', palette='Set2', ax=ax7)
    plt.title(
        'Distribución del Peso Corporal en el Momento de la Eutanasia por Grupo')
    plt.tight_layout()
    figuras.append(fig7)

    # Inicializa el índice de la gráfica actual
    indice_grafica = 0

    # Bucle principal de Pygame
    running = True
    while running:
        mostrar_grafica(indice_grafica)  # Muestra la gráfica actual

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:  # Avanza a la siguiente gráfica
                    indice_grafica = (indice_grafica + 1) % len(figuras)
                elif event.key == pygame.K_LEFT:  # Retrocede a la gráfica anterior
                    indice_grafica = (indice_grafica - 1) % len(figuras)
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:  # Termina el programa
                    from Pantallas.Informacion_Mamiferos import Informacion_Mamiferos
                    from Pantallas.Carga_Graficos import Carga_Graficas
                    Carga_Graficas()
                    Informacion_Mamiferos(db_id)
                    running = False

            # Imprimir el índice actual para depuración
            print(f'Índice actual: {indice_grafica}')

    pygame.quit()
